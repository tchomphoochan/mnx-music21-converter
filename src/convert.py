from music21 import converter, note, stream, meter, duration, chord, pitch, key, beam, clef, articulations, expressions, tempo, bar, repeat, spanner

import music21
from typing import Optional, cast, Union, Tuple, Callable, TypeAlias
import mnx
import logging
log = logging.getLogger(__name__)

# A deferred task takes in an object and decides whether to perform the task.
# If the task has been performed, return True, so the scheduler can remove it from the queue.
Deferred: TypeAlias = Callable[[music21.Music21Object], bool]

class MNXConverter(converter.subConverters.SubConverter):
    registerFormats = ("mnx",)
    registerInputExtensions = ("json",)

    # Maps MNX object IDs to corresponding Music21Object we created (usually notes or chords)
    idMappings: dict[str, music21.Music21Object]

    globalInfo: mnx.Top.Global

    # List of tasks that have been deferred to further in the score.
    tasks: list[Deferred]

    def addTask(self, task: Deferred):
        self.tasks.append(task)

    def runTasks(self, obj: music21.Music21Object):
        doneTasks = [task for task in self.tasks if task(obj)]
        for task in doneTasks:
            self.tasks.remove(task)

    def parseData(self, strData: str, number: int | None = None) -> None:
        # Parse JSON
        top = mnx.Top.from_json(strData)
        assert top.mnx.version == 1, "MNXConverter only supports MNX version 1."

        # Initialize stuff
        self.globalInfo = top.global_
        self.idMappings = {}
        self.tasks = []

        # Walk through the parts to populate notes in measures in voices in parts
        sc = stream.Score()
        for inPart in top.parts:
            outPart = self.parsePart(inPart)
            sc.append(outPart)

        assert len(self.tasks) == 0, "Tasks not empty. Something went wrong."

        # Done. Put the result in self.stream.
        self.stream = sc

    def parsePart(self, inPart: mnx.Top.Part) -> stream.Part:
        outPart = stream.Part()

        outPart.partName = inPart.name
        outPart.partAbbreviation = inPart.short_name
        self.setId(outPart, inPart.id)

        assert inPart.measures is not None, "parts[_].measures is not required but that does not make sense semantically"
        assert self.globalInfo.measures is not None, "global.measures is not required but that does not make sense semantically"
        assert len(inPart.measures) == len(self.globalInfo.measures)

        for inMeas, globalMeas in zip(inPart.measures, self.globalInfo.measures):
            outMeas = self.parseMeasure(inMeas, globalMeas)
            outPart.append(outMeas)

        # TODO: handle .staves
        # TODO: handle .smufl_font
        return outPart

    def parseMeasure(self, inMeas: mnx.Top.Part.Measure, globalMeas: mnx.Top.Global.Measure) -> stream.Measure:
        outMeas = stream.Measure()

        if globalMeas.number is not None:
            outMeas.number = globalMeas.number

        if globalMeas.key is not None:
            k = key.KeySignature(globalMeas.key.fifths)
            # TODO: handle class_
            # TODO: handle color
            outMeas.append(k)

        if globalMeas.time is not None:
            t = meter.TimeSignature(f'{globalMeas.time.count}/{globalMeas.time.unit}')
            outMeas.append(t)

        # I gave up on implementing these jumps.
        # See MNXConverter.parseMeasureLocation for an explanation.
        assert globalMeas.jump is None, "Jump is not supported."
        assert globalMeas.fine is None, "Fine is not supported."
        assert globalMeas.segno is None, "Segno is not supported."

        if globalMeas.tempos is not None:
            for inTempo in globalMeas.tempos:
                # Here, it is not clear what inTempo.location is supposed to represent.
                # I think they meant fraction rather than measure-location?
                assert inTempo.location is not None, "Tempo location not supported"
                outTempo = tempo.MetronomeMark(
                    number=inTempo.bpm,
                    referent=self.parseNoteValue(inTempo.value),
                    # offset=self.parseMeasureLocation(inTempo.location)[1],
                    # offset=self.parseFraction(inTempo.location),
                )
                outMeas.append(outTempo)

        # TODO: handle globalMeas.index
        # I could never figure out what this was supposed to represent.

        # Barline stuff
        if globalMeas.repeat_start is not None:
            rp = bar.Repeat(direction="start")
            outMeas.leftBarline = rp
        if globalMeas.repeat_end is not None:
            rp = bar.Repeat(direction="end")
            rp.times = globalMeas.repeat_end.times
            outMeas.rightBarline = rp
        if globalMeas.barline is not None:
            bl = bar.Barline(type=globalMeas.barline.type)
            outMeas.rightBarline = bl

        # Parse each voice within the measure
        for seq in inMeas.sequences:
            v = self.parseSequence(seq)
            outMeas.append(v)

        # Add beams to the notes
        # TODO: Handle beams across barlines (as it stands right now,
        #       the event lookups fail because things from the future measures aren't available.)
        if inMeas.beams is not None:
            for b in inMeas.beams:
                b = mnx.DefBeam.from_dict(b)
                self.processBeam(b, 1)

        if inMeas.clefs is not None:
            for inClef in inMeas.clefs:
                outClef = self.parseClef(inClef)
                outMeas.insert(outClef)

        # TODO: handle globalMeas.ending
        # if globalMeas.ending is not None:
        #     def addEnding():
        #         numbers = globalMeas.ending.numbers
        #         assert numbers is not None, "It does not make sense for there to be no numbers for endings."
        #         repeat.insertRepeatEnding(self.stream, outMeas.number, outMeas.number+globalMeas.ending.duration-1, numbers)
        #     self.tasks.append(addEnding)

        # If the measure has only one voice, there is no need to have a stream.Voice object.
        return outMeas.flattenUnnecessaryVoices()

    def parseSequence(self, inSeq: mnx.Top.Part.Measure.Sequence) -> stream.Voice:
        outVoice = stream.Voice()

        # handle content, which is a list of events or something similar
        for obj in inSeq.content:
            if isinstance(obj, mnx.DefEvent):
                n = self.parseEvent(obj)
                outVoice.append(n)

            # TODO: handle ContentChoice1 -> Grace note
            # TODO: handle ContentChoice2 -> Tuplet
            # TODO: handle ContentChoice3 -> Octave shift
            # TODO: handle ContentChoice4 -> Space
            # TODO: handle ContentChoice5 -> Dynamic

        # TODO: handle .staff
        # TODO: handle .voice
        # TODO: handle .orient
        return outVoice

    def parseEvent(self, inEvent: mnx.DefEvent) -> note.GeneralNote:
        assert inEvent.type == "event"
        assert inEvent.duration is not None, "An event should have a duration specified"
        dur = self.parseNoteValue(inEvent.duration)
        outNote: note.GeneralNote|None = None

        assert inEvent.notes is not None or inEvent.rest is not None, "An event must have at least a note or a rest."

        if inEvent.notes is not None:
            # NotRest
            assert inEvent.rest is None, "It does not make sense to specify notes and rest at the same time."

            # Get all the notes
            allNotes = []
            for inNote in inEvent.notes:
                n = self.parseNote(inNote)
                n.duration = dur
                allNotes.append(n)
            assert len(allNotes) > 0, "A rest should be specified through .rest field, not .notes"

            # Distinguish between a single note and a chord
            if len(allNotes) == 1:
                # single note
                outNote = allNotes[0]
                self.setId(outNote, inEvent.id, True)  # this will replace the note's ID, but the mapping remains
            else:
                # chord
                c = chord.Chord(allNotes)
                self.setId(c, inEvent.id)  # associate the chord with event
                c.duration = dur
                outNote = c

        elif inEvent.rest is not None:
            # Rest
            assert inEvent.notes is None, "It does not make sense to specify notes and rest at the same time."

            r = note.Rest()
            r.duration = dur
            self.setId(r, inEvent.id)
            outNote = r

        assert outNote is not None

        if inEvent.markings is not None:
            # Interestingly enough, MNX accent has up/down pointing designation for accents
            # but music21 has it for strong accents. Maybe MNX made a mistake here?
            if inEvent.markings.soft_accent is not None:
                raise ValueError("Music21 doesn't have support for soft accent.")
                # or I simply could not find an equivalent one.
            if inEvent.markings.accent is not None:
                outNote.articulations.append(articulations.Accent())
            if inEvent.markings.strong_accent is not None:
                outNote.articulations.append(articulations.StrongAccent())

            # MNX has a field for breath symbol, but it does not specify what those are.
            # Music21 supports 'comma', 'tick', or None.
            # I'm going to assume 'comma' and 'tick' are what MNX intended.
            if inEvent.markings.breath is not None:
                a = articulations.BreathMark()
                a.symbol = inEvent.markings.breath
                outNote.articulations.append(a)

            if inEvent.markings.staccato is not None:
                outNote.articulations.append(articulations.Staccato())
            if inEvent.markings.staccatissimo is not None:
                outNote.articulations.append(articulations.Staccatissimo())
            if inEvent.markings.spiccato is not None:
                outNote.articulations.append(articulations.Spiccato())
            if inEvent.markings.tenuto is not None:
                outNote.articulations.append(articulations.Tenuto())
            if inEvent.markings.unstress is not None:
                outNote.articulations.append(articulations.Unstress())
            if inEvent.markings.stress is not None:
                outNote.articulations.append(articulations.Stress())

            # Interestingly enough, MNX does not seem to have support for
            # multi-note tremolos?
            if inEvent.markings.tremolo is not None:
                e = expressions.Tremolo()
                e.numberOfMarks = inEvent.markings.tremolo.marks

        # TODO: handle .staff
        # TODO: handle .stem_dirction
        # TODO: handle .smufl_font
        # TODO: handle .measure (what even is this?)
        # TODO: handle .orient

        # Slurs
        if inEvent.slurs is not None:
            for slur in inEvent.slurs:
                self.queueSlur(outNote, slur)

        return outNote

    def queueSlur(self, start: note.GeneralNote, slur: mnx.DefEvent.Slur):
        def task(end: music21.Music21Object) -> bool:
            # We add slur as soon as the target note is found.
            if end.id != slur.target:
                return False
            assert isinstance(end, note.GeneralNote)

            # Need to make a separate copy because
            # otherwise start.sites contains the slur itself.
            sites = list(start.sites)

            # There are two kinds of slurs: Slurs that are tied from an event to another event,
            # and slurs that are additionally associated with specific notes.
            # I don't think Music21 supports the second kind.
            sp = spanner.Slur()
            if slur.start_note is None:
                assert slur.end_note is None, "Slurs at specific notes must have both start_note and end_note"
                sp.addSpannedElements(start)
                sp.addSpannedElements(end)
            else:
                assert slur.end_note is not None, "Slurs at specific notes must have both start_note and end_note"
                log.warning(f"Specific-note slur from {slur.start_note} to {slur.end_note} is omitted.")
                # sp.addSpannedElements(self.lookup(slur.start_note))
                # sp.addSpannedElements(self.lookup(slur.end_note))
                sp.addSpannedElements(start)
                sp.addSpannedElements(end)

            # MNX did not document lineType, but it seems to be
            # directly inspired by MusicXML.
            sp.lineType = slur.line_type

            if slur.side is not None:
                sp.placement = {
                    'up': 'above',
                    'down': 'below'
                }[slur.side]

            # TODO: Handle .side_end (not sure what it means).

            # TODO: Handle incomplete slur with .location (can't find how Music21 represents this).

            # Now actually add the slur.
            for site in sites:
                site.append(sp)
            return True

        if slur.target is None:
            log.warning(f"An incomplete slur is omitted.")
        else:
            self.addTask(task)

    def parseNoteValue(self, inDur: mnx.DefNoteValue) -> duration.Duration:
        # In Music21, duration types are defined in duration.py:137.
        # It seems like MNX takes inspiration directly from this.
        mnxToM21Type: dict[str, str] = {
            'duplex-maxima': 'duplex-maxima',
            'maxima': 'maxima',
            'longa': 'longa',
            'breve': 'breve',
            'whole': 'whole',
            'half': 'half',
            'quarter': 'quarter',
            'eighth': 'eighth',
            '16th': '16th',
            '32nd': '32nd',
            '64th': '64th',
            '128th': '128th',
            '256th': '256th',
            '512th': '512th',
            '1024th': '1024th',
            '2048th': '2048th',
        }
        if inDur.base == '4096th':
            raise ValueError("MNX has 4096th but music21 only supports up to 2048th")

        return duration.Duration(
            type=mnxToM21Type[inDur.base],
            dots=0 if inDur.dots is None else inDur.dots,
        )

    def parseNote(self, inNote: mnx.DefEvent.Note) -> note.Note:
        outNote = note.Note()

        # handle the pitch
        outNote.pitch = pitch.Pitch(step=inNote.pitch.step,
                                    octave=inNote.pitch.octave)

        if inNote.pitch.alter is not None:
            outNote.pitch.accidental = pitch.Accidental(inNote.pitch.alter)

        # handle the marking for accidental display
        if inNote.accidental_display is not None:
            if inNote.accidental_display.show:
                if outNote.pitch.accidental is None:
                    outNote.pitch.accidental = pitch.Accidental(0)
                outNote.pitch.accidental.displayType = 'always'

        self.setId(outNote, inNote.id)

        # TODO: handle .class_
        # TODO: handle .perform
        # TODO: handle .tie
        # TODO: handle .staff
        # TODO: handle .accidental_display.editorial
        # TODO: handle .accidental_display.cautionary
        # TODO: handle .smufl_font

        return outNote

    def processBeam(self, inBeam: mnx.DefBeam, level: int) -> None:

        # Add full beams
        assert len(inBeam.events), "A beam must consist of at least one events; use a hook instead."
        for i, eventId in enumerate(inBeam.events):
            even = self.lookup(eventId)
            assert isinstance(even, note.NotRest)

            beamType: str
            if i == 0:
                beamType = 'start'
            elif i == len(inBeam.events)-1:
                beamType = 'stop'
            else:
                beamType = 'continue'
            even.beams.append(beam.Beam(type=beamType, number=level))

        # Add inner beams
        if inBeam.inner is not None:
            assert inBeam.hooks is None, "It does not make sense for inner beams and hooks to be specified at the same level."
            for n in inBeam.inner:
                n = mnx.DefBeam.from_dict(n)
                self.processBeam(n, level+1)

        # Add hooks
        if inBeam.hooks is not None:
            assert inBeam.inner is None, "It does not make sense for inner beams and hooks to be specified at the same level."
            for hook in inBeam.hooks:
                n = self.lookup(hook.event)
                assert isinstance(n, note.NotRest)
                n.beams.append(beam.Beam(type="partial", direction=hook.direction, number=level+1))

    def parseClef(self, inClef: mnx.Top.Part.Measure.Clef) -> clef.Clef:
        signToClefType: dict[str, clef.Clef] = {
            'C': clef.CClef(),
            'F': clef.FClef(),
            'G': clef.GClef(),
        }
        outClef = signToClefType[inClef.clef.sign]

        # How to specify clef position isn't clear from the MNX spec.
        # My understanding is that 0 refers to the center line, -1 refers to
        # the gap below, -2 refers to the line below (e.g. Treble clef), ...
        # Positive numbers refer to spaces or lines above.
        # Meanwhile, for Music21, the bottom line is line 1, next line up is 2, ...
        # There doesn't seem to be any support for clefs that go in between lines.
        pos = 3 + inClef.clef.staff_position/2
        assert pos % 1.0 == 0.0, "Music21 only supports clefs on lines, not spaces."
        pos = int(pos)
        outClef.line = pos

        if inClef.position is not None:
            outClef.offset = self.parseFraction(inClef.position.fraction)
            # TODO: handle inClef.position.grace_index

        return outClef

    def parseMeasureLocation(self, text: mnx.DefMeasureLocation) -> Tuple[int, Optional[float]]:
        # MNX never properly specifies what this string should look like.
        # The examples are quite contradictory.
        parts = text.split(':')

        # Example 1: https://w3c.github.io/mnx/docs/comparisons/musicxml/#octave-shifts-8va.
        # It seems the expected form is <measureNumber>:<position>/<base>,
        # signifying the absolute position of the end of the 8va spanner.
        # The measure "index" (as mentioned in the example0 seems to start from 1.
        if len(parts) == 2:
            measureNumber = int(parts[0])
            offset = self.parseFraction([int(x) for x in parts[1]])

            # returns index starting from 0 and offset
            return measureNumber-1, offset

        # Example 2: https://w3c.github.io/mnx/docs/comparisons/musicxml/#jumps-dal-segno
        # Example 3: https://w3c.github.io/mnx/docs/comparisons/musicxml/#jumps-ds-al-fine
        # Those two example only use <measureNumber>, no metrical position.
        # Jump points specify the target locations. Measure numbers seem to start from 0.
        # It is unclear what the segno symbol and the fine text's locations
        # are meant to represent.
        if len(parts) == 1:
            # returns index starting from 0 and no offset
            return int(parts[0]), None

        raise ValueError("Can't parse measure location.")

    def parseFraction(self, frac: list[int]) -> float:
        # MNX never specifies how to read fractions.
        # In fact, it never says that fraction has to be a list of two elements.
        # Therefore, I'm making assumptions here.
        assert len(frac) == 2, "Fraction has to have exactly two elements."
        return frac[0]/frac[1]

    def setId(self, obj: music21.Music21Object, ident: Optional[str], allowShadowing: bool = False) -> None:
        # ident stands for identifier
        if ident is None:
            return

        if ident in self.idMappings:
            raise KeyError(ident, obj, "Identifier already exists in the ID mapping.")

        if not allowShadowing:
            if obj.id in self.idMappings:
                raise ValueError(ident, obj, "The object already has an existing identifier. Should not rewrite.")

        obj.id = ident
        self.idMappings[ident] = obj
        self.runTasks(obj)

    def lookup(self, ident: str) -> music21.Music21Object:
        if ident not in self.idMappings:
            raise KeyError(ident, "Identifier does not exist in the ID mappings")
        return self.idMappings[ident]

converter.registerSubConverter(MNXConverter)

if __name__ == "__main__":
    s: str
    with open('../examples/bach_minuet.json', 'r') as f:
        s = f.read()
    sc = converter.parse(s, format="mnx")
    sc.show('t')
    # sc.show('musicxml.pdf', makeNotation=False)
    sc.show(makeNotation=False)
