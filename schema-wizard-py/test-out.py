from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import *
from dataclass_wizard import JSONWizard, json_field  # mypy: ignore

DefPositiveInteger = int


@dataclass
class DefNoteValue(JSONWizard):
    Base = str
    # Required fields
    base: Base = json_field(["base"])
    # Optional fields
    dots: DefPositiveInteger = json_field(["dots"], default_factory=DefPositiveInteger)


DefColor = str

DefId = str

DefIntegerUnsigned = int

DefMeasureLocation = str

DefMeasureNumber = int

DefOrientation = str

DefSlurSide = str

DefSlurTieEndLocation = str

DefSmuflFont = str

DefSmuflGlyph = str

DefStaffLabel = str

DefStaffLabelref = str

DefStaffNumber = int

DefStaffPosition = int

DefStaffSymbol = str

DefStemDirection = str

DefStyleClass = str

DefTupletDisplaySetting = str

DefUpOrDown = str

DefVoiceName = str


@dataclass
class DefBeamList(JSONWizard):
    @dataclass
    class Hook(JSONWizard):
        Direction = str
        # Required fields
        direction: Direction = json_field(["direction"])
        event: DefId = json_field(["event"])
        # Optional fields
        pass

    # Required fields
    events: list[DefId] = json_field(["events"])
    # Optional fields
    hooks: list[Hook] = json_field(["hooks"], default_factory=list)
    inner: "DefBeamList" = json_field(["inner"], default_factory=lambda *args: None)


@dataclass
class DefEvent(JSONWizard):
    @dataclass
    class Markings(JSONWizard):
        @dataclass
        class Accent(JSONWizard):
            # Required fields
            pass
            # Optional fields
            pointing: DefUpOrDown = json_field(
                ["pointing"], default_factory=DefUpOrDown
            )

        @dataclass
        class Breath(JSONWizard):
            Symbol = str
            # Required fields
            pass
            # Optional fields
            symbol: Symbol = json_field(["symbol"], default_factory=Symbol)

        @dataclass
        class SoftAccent(JSONWizard):
            # Required fields
            pass
            # Optional fields
            pass

        @dataclass
        class Spiccato(JSONWizard):
            # Required fields
            pass
            # Optional fields
            pass

        @dataclass
        class Staccatissimo(JSONWizard):
            # Required fields
            pass
            # Optional fields
            pass

        @dataclass
        class Staccato(JSONWizard):
            # Required fields
            pass
            # Optional fields
            pass

        @dataclass
        class Stress(JSONWizard):
            # Required fields
            pass
            # Optional fields
            pass

        @dataclass
        class StrongAccent(JSONWizard):
            # Required fields
            pass
            # Optional fields
            pointing: DefUpOrDown = json_field(
                ["pointing"], default_factory=DefUpOrDown
            )

        @dataclass
        class Tenuto(JSONWizard):
            # Required fields
            pass
            # Optional fields
            pass

        @dataclass
        class Tremolo(JSONWizard):
            # Required fields
            marks: DefPositiveInteger = json_field(["marks"])
            # Optional fields
            pass

        @dataclass
        class Unstress(JSONWizard):
            # Required fields
            pass
            # Optional fields
            pass

        # Required fields
        pass
        # Optional fields
        accent: Accent = json_field(["accent"], default_factory=Accent)
        breath: Breath = json_field(["breath"], default_factory=Breath)
        softAccent: SoftAccent = json_field(["softAccent"], default_factory=SoftAccent)
        spiccato: Spiccato = json_field(["spiccato"], default_factory=Spiccato)
        staccatissimo: Staccatissimo = json_field(
            ["staccatissimo"], default_factory=Staccatissimo
        )
        staccato: Staccato = json_field(["staccato"], default_factory=Staccato)
        stress: Stress = json_field(["stress"], default_factory=Stress)
        strongAccent: StrongAccent = json_field(
            ["strongAccent"], default_factory=StrongAccent
        )
        tenuto: Tenuto = json_field(["tenuto"], default_factory=Tenuto)
        tremolo: Tremolo = json_field(["tremolo"], default_factory=Tremolo)
        unstress: Unstress = json_field(["unstress"], default_factory=Unstress)

    Measure = bool

    @dataclass
    class Note(JSONWizard):
        @dataclass
        class AccidentalDisplay(JSONWizard):
            Cautionary = bool
            Editorial = bool
            Show = bool
            # Required fields
            show: Show = json_field(["show"])
            # Optional fields
            cautionary: Cautionary = json_field(
                ["cautionary"], default_factory=Cautionary
            )
            editorial: Editorial = json_field(["editorial"], default_factory=Editorial)

        @dataclass
        class Perform(JSONWizard):
            # Required fields
            pass
            # Optional fields
            pass

        @dataclass
        class Pitch(JSONWizard):
            Alter = int
            Octave = int
            Step = str
            # Required fields
            octave: Octave = json_field(["octave"])
            step: Step = json_field(["step"])
            # Optional fields
            alter: Alter = json_field(["alter"], default_factory=Alter)

        @dataclass
        class Tie(JSONWizard):
            # Required fields
            pass
            # Optional fields
            location: DefSlurTieEndLocation = json_field(
                ["location"], default_factory=DefSlurTieEndLocation
            )
            target: DefId = json_field(["target"], default_factory=DefId)

        # Required fields
        pitch: Pitch = json_field(["pitch"])
        # Optional fields
        accidentalDisplay: AccidentalDisplay = json_field(
            ["accidentalDisplay"], default_factory=AccidentalDisplay
        )
        _class: DefStyleClass = json_field(["class"], default_factory=DefStyleClass)
        id: DefId = json_field(["id"], default_factory=DefId)
        perform: Perform = json_field(["perform"], default_factory=Perform)
        smuflFont: DefSmuflFont = json_field(
            ["smuflFont"], default_factory=DefSmuflFont
        )
        staff: DefStaffNumber = json_field(["staff"], default_factory=DefStaffNumber)
        tie: Tie = json_field(["tie"], default_factory=Tie)

    @dataclass
    class Rest(JSONWizard):
        # Required fields
        pass
        # Optional fields
        staffPosition: DefStaffPosition = json_field(
            ["staffPosition"], default_factory=DefStaffPosition
        )

    @dataclass
    class Slur(JSONWizard):
        LineType = str
        # Required fields
        pass
        # Optional fields
        endNote: DefId = json_field(["endNote"], default_factory=DefId)
        lineType: LineType = json_field(["lineType"], default_factory=LineType)
        location: DefSlurTieEndLocation = json_field(
            ["location"], default_factory=DefSlurTieEndLocation
        )
        side: DefSlurSide = json_field(["side"], default_factory=DefSlurSide)
        sideEnd: DefSlurSide = json_field(["sideEnd"], default_factory=DefSlurSide)
        startNote: DefId = json_field(["startNote"], default_factory=DefId)
        target: DefId = json_field(["target"], default_factory=DefId)

    Type = str
    # Required fields
    _type: Type = json_field(["type"])
    # Optional fields
    duration: DefNoteValue = json_field(["duration"], default_factory=DefNoteValue)
    id: DefId = json_field(["id"], default_factory=DefId)
    markings: Markings = json_field(["markings"], default_factory=Markings)
    measure: Measure = json_field(["measure"], default_factory=Measure)
    notes: list[Note] = json_field(["notes"], default_factory=list)
    orient: DefOrientation = json_field(["orient"], default_factory=DefOrientation)
    rest: Rest = json_field(["rest"], default_factory=Rest)
    slurs: list[Slur] = json_field(["slurs"], default_factory=list)
    smuflFont: DefSmuflFont = json_field(["smuflFont"], default_factory=DefSmuflFont)
    staff: DefStaffNumber = json_field(["staff"], default_factory=DefStaffNumber)
    stemDirection: DefStemDirection = json_field(
        ["stemDirection"], default_factory=DefStemDirection
    )


@dataclass
class DefNoteValueQuantity(JSONWizard):
    # Required fields
    duration: DefNoteValue = json_field(["duration"])
    multiple: DefPositiveInteger = json_field(["multiple"])
    # Optional fields
    pass


@dataclass
class DefSystemLayoutContentChoice00(JSONWizard):
    Type = str
    # Required fields
    content: "DefSystemLayoutContent" = json_field(["content"])
    _type: Type = json_field(["type"])
    # Optional fields
    label: DefStaffLabel = json_field(["label"], default_factory=DefStaffLabel)
    symbol: DefStaffSymbol = json_field(["symbol"], default_factory=DefStaffSymbol)


@dataclass
class DefSystemLayoutContentChoice01(JSONWizard):
    @dataclass
    class Source(JSONWizard):
        # Required fields
        part: DefId = json_field(["part"])
        # Optional fields
        label: DefStaffLabel = json_field(["label"], default_factory=DefStaffLabel)
        labelref: DefStaffLabelref = json_field(
            ["labelref"], default_factory=DefStaffLabelref
        )
        staff: DefStaffNumber = json_field(["staff"], default_factory=DefStaffNumber)
        stem: DefStemDirection = json_field(["stem"], default_factory=DefStemDirection)
        voice: DefVoiceName = json_field(["voice"], default_factory=DefVoiceName)

    Type = str
    # Required fields
    sources: list[Source] = json_field(["sources"])
    _type: Type = json_field(["type"])
    # Optional fields
    label: DefStaffLabel = json_field(["label"], default_factory=DefStaffLabel)
    labelref: DefStaffLabelref = json_field(
        ["labelref"], default_factory=DefStaffLabelref
    )
    symbol: DefStaffSymbol = json_field(["symbol"], default_factory=DefStaffSymbol)


DefSystemLayoutContent = Union[
    DefSystemLayoutContentChoice00, DefSystemLayoutContentChoice01
]


@dataclass
class MnxDocument(JSONWizard):
    @dataclass
    class Global(JSONWizard):
        @dataclass
        class Measure(JSONWizard):
            @dataclass
            class Barline(JSONWizard):
                Type = str
                # Required fields
                _type: Type = json_field(["type"])
                # Optional fields
                pass

            @dataclass
            class Ending(JSONWizard):
                Duration = int
                Number = int
                Open = bool
                # Required fields
                duration: Duration = json_field(["duration"])
                # Optional fields
                _class: DefStyleClass = json_field(
                    ["class"], default_factory=DefStyleClass
                )
                color: DefColor = json_field(["color"], default_factory=DefColor)
                numbers: list[Number] = json_field(["numbers"], default_factory=list)
                open: Open = json_field(["open"], default_factory=Open)

            @dataclass
            class Fine(JSONWizard):
                # Required fields
                location: DefMeasureLocation = json_field(["location"])
                # Optional fields
                _class: DefStyleClass = json_field(
                    ["class"], default_factory=DefStyleClass
                )
                color: DefColor = json_field(["color"], default_factory=DefColor)

            @dataclass
            class Jump(JSONWizard):
                Type = str
                # Required fields
                location: DefMeasureLocation = json_field(["location"])
                _type: Type = json_field(["type"])
                # Optional fields
                pass

            @dataclass
            class Key(JSONWizard):
                Fifths = int
                # Required fields
                fifths: Fifths = json_field(["fifths"])
                # Optional fields
                _class: DefStyleClass = json_field(
                    ["class"], default_factory=DefStyleClass
                )
                color: DefColor = json_field(["color"], default_factory=DefColor)

            @dataclass
            class RepeatEnd(JSONWizard):
                Times = int
                # Required fields
                pass
                # Optional fields
                times: Times = json_field(["times"], default_factory=Times)

            @dataclass
            class RepeatStart(JSONWizard):
                # Required fields
                pass
                # Optional fields
                pass

            @dataclass
            class Segno(JSONWizard):
                # Required fields
                location: DefMeasureLocation = json_field(["location"])
                # Optional fields
                _class: DefStyleClass = json_field(
                    ["class"], default_factory=DefStyleClass
                )
                color: DefColor = json_field(["color"], default_factory=DefColor)
                glyph: DefSmuflGlyph = json_field(
                    ["glyph"], default_factory=DefSmuflGlyph
                )

            @dataclass
            class Tempo(JSONWizard):
                Bpm = int
                # Required fields
                bpm: Bpm = json_field(["bpm"])
                value: DefNoteValue = json_field(["value"])
                # Optional fields
                location: DefMeasureLocation = json_field(
                    ["location"], default_factory=DefMeasureLocation
                )

            @dataclass
            class Time(JSONWizard):
                Unit = int
                # Required fields
                count: DefPositiveInteger = json_field(["count"])
                unit: Unit = json_field(["unit"])
                # Optional fields
                pass

            # Required fields
            pass
            # Optional fields
            barline: Barline = json_field(["barline"], default_factory=Barline)
            ending: Ending = json_field(["ending"], default_factory=Ending)
            fine: Fine = json_field(["fine"], default_factory=Fine)
            index: DefMeasureNumber = json_field(
                ["index"], default_factory=DefMeasureNumber
            )
            jump: Jump = json_field(["jump"], default_factory=Jump)
            key: Key = json_field(["key"], default_factory=Key)
            number: DefMeasureNumber = json_field(
                ["number"], default_factory=DefMeasureNumber
            )
            repeatEnd: RepeatEnd = json_field(["repeatEnd"], default_factory=RepeatEnd)
            repeatStart: RepeatStart = json_field(
                ["repeatStart"], default_factory=RepeatStart
            )
            segno: Segno = json_field(["segno"], default_factory=Segno)
            tempos: list[Tempo] = json_field(["tempos"], default_factory=list)
            time: Time = json_field(["time"], default_factory=Time)

        @dataclass
        class Style(JSONWizard):
            Selector = str
            # Required fields
            selector: Selector = json_field(["selector"])
            # Optional fields
            color: DefColor = json_field(["color"], default_factory=DefColor)

        # Required fields
        measures: list[Measure] = json_field(["measures"])
        # Optional fields
        styles: list[Style] = json_field(["styles"], default_factory=list)

    @dataclass
    class Layout(JSONWizard):
        # Required fields
        content: DefSystemLayoutContent = json_field(["content"])
        id: DefId = json_field(["id"])
        # Optional fields
        pass

    @dataclass
    class Mnx(JSONWizard):
        Version = int
        # Required fields
        version: Version = json_field(["version"])
        # Optional fields
        pass

    @dataclass
    class Part(JSONWizard):
        @dataclass
        class Measure(JSONWizard):
            @dataclass
            class Clef(JSONWizard):
                @dataclass
                class Clef(JSONWizard):
                    Color = str
                    Octave = int
                    Sign = str
                    # Required fields
                    sign: Sign = json_field(["sign"])
                    staffPosition: DefStaffPosition = json_field(["staffPosition"])
                    # Optional fields
                    _class: DefStyleClass = json_field(
                        ["class"], default_factory=DefStyleClass
                    )
                    color: Color = json_field(["color"], default_factory=Color)
                    glyph: DefSmuflGlyph = json_field(
                        ["glyph"], default_factory=DefSmuflGlyph
                    )
                    octave: Octave = json_field(["octave"], default_factory=Octave)

                @dataclass
                class Position(JSONWizard):
                    # Required fields
                    fraction: list[DefIntegerUnsigned] = json_field(["fraction"])
                    # Optional fields
                    graceIndex: DefIntegerUnsigned = json_field(
                        ["graceIndex"], default_factory=DefIntegerUnsigned
                    )

                # Required fields
                clef: Clef = json_field(["clef"])
                # Optional fields
                position: Position = json_field(["position"], default_factory=Position)

            @dataclass
            class Sequence(JSONWizard):
                @dataclass
                class ContentChoice01(JSONWizard):
                    GraceType = str
                    Slash = bool
                    Type = str
                    # Required fields
                    content: list[DefEvent] = json_field(["content"])
                    _type: Type = json_field(["type"])
                    # Optional fields
                    _class: DefStyleClass = json_field(
                        ["class"], default_factory=DefStyleClass
                    )
                    color: DefColor = json_field(["color"], default_factory=DefColor)
                    graceType: GraceType = json_field(
                        ["graceType"], default_factory=GraceType
                    )
                    slash: Slash = json_field(["slash"], default_factory=Slash)

                @dataclass
                class ContentChoice02(JSONWizard):
                    Bracket = str
                    Type = str
                    # Required fields
                    content: list[DefEvent] = json_field(["content"])
                    inner: DefNoteValueQuantity = json_field(["inner"])
                    outer: DefNoteValueQuantity = json_field(["outer"])
                    _type: Type = json_field(["type"])
                    # Optional fields
                    bracket: Bracket = json_field(["bracket"], default_factory=Bracket)
                    orient: DefOrientation = json_field(
                        ["orient"], default_factory=DefOrientation
                    )
                    showNumber: DefTupletDisplaySetting = json_field(
                        ["showNumber"], default_factory=DefTupletDisplaySetting
                    )
                    showValue: DefTupletDisplaySetting = json_field(
                        ["showValue"], default_factory=DefTupletDisplaySetting
                    )
                    staff: DefStaffNumber = json_field(
                        ["staff"], default_factory=DefStaffNumber
                    )

                @dataclass
                class ContentChoice03(JSONWizard):
                    Type = str
                    Value = int
                    # Required fields
                    end: DefMeasureLocation = json_field(["end"])
                    _type: Type = json_field(["type"])
                    value: Value = json_field(["value"])
                    # Optional fields
                    orient: DefOrientation = json_field(
                        ["orient"], default_factory=DefOrientation
                    )
                    staff: DefStaffNumber = json_field(
                        ["staff"], default_factory=DefStaffNumber
                    )

                @dataclass
                class ContentChoice04(JSONWizard):
                    Type = str
                    # Required fields
                    duration: DefNoteValueQuantity = json_field(["duration"])
                    _type: Type = json_field(["type"])
                    # Optional fields
                    pass

                @dataclass
                class ContentChoice05(JSONWizard):
                    Type = str
                    Value = str
                    # Required fields
                    _type: Type = json_field(["type"])
                    value: Value = json_field(["value"])
                    # Optional fields
                    glyph: DefSmuflGlyph = json_field(
                        ["glyph"], default_factory=DefSmuflGlyph
                    )

                Content = Union[
                    DefEvent,
                    ContentChoice01,
                    ContentChoice02,
                    ContentChoice03,
                    ContentChoice04,
                    ContentChoice05,
                ]
                # Required fields
                content: list[Content] = json_field(["content"])
                # Optional fields
                orient: DefOrientation = json_field(
                    ["orient"], default_factory=DefOrientation
                )
                staff: DefStaffNumber = json_field(
                    ["staff"], default_factory=DefStaffNumber
                )
                voice: DefVoiceName = json_field(
                    ["voice"], default_factory=DefVoiceName
                )

            # Required fields
            sequences: list[Sequence] = json_field(["sequences"])
            # Optional fields
            beams: DefBeamList = json_field(["beams"], default_factory=DefBeamList)
            clefs: list[Clef] = json_field(["clefs"], default_factory=list)

        Name = str
        ShortName = str
        Staves = int
        # Required fields
        pass
        # Optional fields
        id: DefId = json_field(["id"], default_factory=DefId)
        measures: list[Measure] = json_field(["measures"], default_factory=list)
        name: Name = json_field(["name"], default_factory=Name)
        shortName: ShortName = json_field(["shortName"], default_factory=ShortName)
        smuflFont: DefSmuflFont = json_field(
            ["smuflFont"], default_factory=DefSmuflFont
        )
        staves: Staves = json_field(["staves"], default_factory=Staves)

    @dataclass
    class Score(JSONWizard):
        @dataclass
        class MultimeasureRest(JSONWizard):
            Duration = int
            Label = str
            # Required fields
            duration: Duration = json_field(["duration"])
            start: DefMeasureNumber = json_field(["start"])
            # Optional fields
            label: Label = json_field(["label"], default_factory=Label)

        Name = str

        @dataclass
        class Page(JSONWizard):
            @dataclass
            class System(JSONWizard):
                @dataclass
                class LayoutChange(JSONWizard):
                    # Required fields
                    layout: DefId = json_field(["layout"])
                    location: DefMeasureLocation = json_field(["location"])
                    # Optional fields
                    pass

                # Required fields
                measure: DefMeasureNumber = json_field(["measure"])
                # Optional fields
                layout: DefId = json_field(["layout"], default_factory=DefId)
                layoutChanges: list[LayoutChange] = json_field(
                    ["layoutChanges"], default_factory=list
                )

            # Required fields
            systems: list[System] = json_field(["systems"])
            # Optional fields
            layout: DefId = json_field(["layout"], default_factory=DefId)

        # Required fields
        name: Name = json_field(["name"])
        # Optional fields
        layout: DefId = json_field(["layout"], default_factory=DefId)
        multimeasureRests: list[MultimeasureRest] = json_field(
            ["multimeasureRests"], default_factory=list
        )
        pages: list[Page] = json_field(["pages"], default_factory=list)

    # Required fields
    _global: Global = json_field(["global"])
    mnx: Mnx = json_field(["mnx"])
    parts: list[Part] = json_field(["parts"])
    # Optional fields
    layouts: list[Layout] = json_field(["layouts"], default_factory=list)
    scores: list[Score] = json_field(["scores"], default_factory=list)


import json

with open("examples/bach_minuet.json", "r") as f:
    d = json.load(f)

d = MnxDocument.from_dict(d)
print(d)
