from typing import Optional

import music21
from music21 import converter, note, stream, meter, duration, chord, pitch, key
import json
import mnx


class MNXConverter(converter.subConverters.SubConverter):
    registerFormats = ("mnx",)
    registerInputExtensions = ("json",)

    idMappings: dict[str, music21.Music21Object]
    globalInfo: mnx.Top.Global

    def parseData(self, strData: str, number: int | None = None) -> None:
        # Parse JSON
        top = mnx.Top.from_json(strData)
        assert top.mnx.version == 1, "MNXConverter only supports MNX version 1."

        # Initialize stuff
        self.globalInfo = top.global_
        self.idMappings = {}

        # Walk through the parts to populate notes in measures in voices in parts
        sc = stream.Score()
        for inPart in top.parts:
            outPart = self.parsePart(inPart)
            sc.append(outPart)

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

        # TODO: handle globalMeas.jump
        # TODO: handle globalMeas.fine
        # TODO: handle globalMeas.tempos
        # TODO: handle globalMeas.ending
        # TODO: handle globalMeas.barline
        # TODO: handle globalMeas.index
        # TODO: handle globalMeas.repeat_start
        # TODO: handle globalMeas.time
        # TODO: handle globalMeas.key
        # TODO: handle globalMeas.segno
        # TODO: handle globalMeas.repeat_end

        for seq in inMeas.sequences:
            v = self.parseSequence(seq)
            outMeas.append(v)

        # TODO: handle inMeas.beams
        # TODO: handle inMeas.clefs

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
                n = allNotes[0]
                self.setId(n, inEvent.id)  # this will replace the note's ID, but the mapping remains
                return n
            else:
                # chord
                c = chord.Chord(allNotes)
                self.setId(c, inEvent.id)  # associate the chord with event
                c.duration = dur
                return c

        if inEvent.rest is not None:
            # Rest
            assert inEvent.notes is None, "It does not make sense to specify notes and rest at the same time."

            r = note.Rest()
            r.duration = dur
            self.setId(r, inEvent.id)
            return r

        # TODO: handle .staff
        # TODO: handle .stem_dirction
        # TODO: handle .smufl_font
        # TODO: handle .measure (what even is this?)
        # TODO: handle .orient
        # TODO: handle .markings
        # TODO: handle .slurs
        assert False, "Should not reach here"

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

    def setId(self, obj: music21.Music21Object, value: Optional[str]) -> None:
        if value is not None:
            obj.id = value
            self.idMappings[value] = obj


converter.registerSubConverter(MNXConverter)

s = ""
with open('../examples/bach_minuet.json', 'r') as f:
    s = f.read()
sc = converter.parse(s, format="mnx")
sc.show('t')
sc.show('musicxml.pdf', makeNotation=False)
