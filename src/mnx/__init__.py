from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import *
from dataclass_wizard import JSONWizard, json_field  # type: ignore

DefStyleClass: TypeAlias = str
DefMeasureLocation: TypeAlias = str
DefSmuflFont: TypeAlias = str
DefSlurSide: TypeAlias = Literal["up", "down"]
DefStaffNumber: TypeAlias = int
DefPositiveInteger: TypeAlias = int


@dataclass
class DefNoteValue(JSONWizard):
    # required fields:
    base: Literal[
        "duplexMaxima",
        "maxima",
        "longa",
        "breve",
        "whole",
        "half",
        "quarter",
        "eighth",
        "16th",
        "32nd",
        "64th",
        "128th",
        "256th",
        "512th",
        "1024th",
        "2048th",
        "4096th",
    ] = json_field(["base"])
    # optional fields:
    dots: Optional[DefPositiveInteger] = json_field(["dots"], default=None)


DefSlurTieEndLocation: TypeAlias = str
DefStemDirection: TypeAlias = Literal["up", "down"]
DefId: TypeAlias = str
DefUpOrDown: TypeAlias = Literal["up", "down"]
DefOrientation: TypeAlias = str
DefStaffPosition: TypeAlias = int


@dataclass
class DefEvent(JSONWizard):
    @dataclass
    class Slur(JSONWizard):
        # required fields:
        # optional fields:
        end_note: Optional[DefId] = json_field(["endNote"], default=None)
        location: Optional[DefSlurTieEndLocation] = json_field(
            ["location"], default=None
        )
        start_note: Optional[DefId] = json_field(["startNote"], default=None)
        side: Optional[DefSlurSide] = json_field(["side"], default=None)
        side_end: Optional[DefSlurSide] = json_field(["sideEnd"], default=None)
        target: Optional[DefId] = json_field(["target"], default=None)
        line_type: Optional[str] = json_field(["lineType"], default=None)

    @dataclass
    class Note(JSONWizard):
        @dataclass
        class Tie(JSONWizard):
            # required fields:
            # optional fields:
            location: Optional[DefSlurTieEndLocation] = json_field(
                ["location"], default=None
            )
            target: Optional[DefId] = json_field(["target"], default=None)

        @dataclass
        class AccidentalDisplay(JSONWizard):
            # required fields:
            show: bool = json_field(["show"])
            # optional fields:
            cautionary: Optional[bool] = json_field(["cautionary"], default=None)
            editorial: Optional[bool] = json_field(["editorial"], default=None)

        @dataclass
        class Perform(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Pitch(JSONWizard):
            # required fields:
            octave: int = json_field(["octave"])
            step: Literal["A", "B", "C", "D", "E", "F", "G"] = json_field(["step"])
            # optional fields:
            alter: Optional[int] = json_field(["alter"], default=None)

        # required fields:
        pitch: Pitch = json_field(["pitch"])
        # optional fields:
        staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
        perform: Optional[Perform] = json_field(["perform"], default=None)
        accidental_display: Optional[AccidentalDisplay] = json_field(
            ["accidentalDisplay"], default=None
        )
        smufl_font: Optional[DefSmuflFont] = json_field(["smuflFont"], default=None)
        id: Optional[DefId] = json_field(["id"], default=None)
        class_: Optional[DefStyleClass] = json_field(["class"], default=None)
        tie: Optional[Tie] = json_field(["tie"], default=None)

    @dataclass
    class Rest(JSONWizard):
        # required fields:
        # optional fields:
        staff_position: Optional[DefStaffPosition] = json_field(
            ["staffPosition"], default=None
        )

    @dataclass
    class Markings(JSONWizard):
        @dataclass
        class Tenuto(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Spiccato(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Breath(JSONWizard):
            # required fields:
            # optional fields:
            symbol: Optional[str] = json_field(["symbol"], default=None)

        @dataclass
        class Unstress(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Accent(JSONWizard):
            # required fields:
            # optional fields:
            pointing: Optional[DefUpOrDown] = json_field(["pointing"], default=None)

        @dataclass
        class Staccatissimo(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class SoftAccent(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Staccato(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Stress(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class StrongAccent(JSONWizard):
            # required fields:
            # optional fields:
            pointing: Optional[DefUpOrDown] = json_field(["pointing"], default=None)

        @dataclass
        class Tremolo(JSONWizard):
            # required fields:
            marks: DefPositiveInteger = json_field(["marks"])
            # optional fields:

        # required fields:
        # optional fields:
        accent: Optional[Accent] = json_field(["accent"], default=None)
        tremolo: Optional[Tremolo] = json_field(["tremolo"], default=None)
        unstress: Optional[Unstress] = json_field(["unstress"], default=None)
        spiccato: Optional[Spiccato] = json_field(["spiccato"], default=None)
        stress: Optional[Stress] = json_field(["stress"], default=None)
        staccatissimo: Optional[Staccatissimo] = json_field(
            ["staccatissimo"], default=None
        )
        strong_accent: Optional[StrongAccent] = json_field(
            ["strongAccent"], default=None
        )
        staccato: Optional[Staccato] = json_field(["staccato"], default=None)
        tenuto: Optional[Tenuto] = json_field(["tenuto"], default=None)
        soft_accent: Optional[SoftAccent] = json_field(["softAccent"], default=None)
        breath: Optional[Breath] = json_field(["breath"], default=None)

    # required fields:
    type: Literal["event"] = json_field(["type"])
    # optional fields:
    notes: Optional[list[Note]] = json_field(["notes"], default=None)
    id: Optional[DefId] = json_field(["id"], default=None)
    smufl_font: Optional[DefSmuflFont] = json_field(["smuflFont"], default=None)
    orient: Optional[DefOrientation] = json_field(["orient"], default=None)
    markings: Optional[Markings] = json_field(["markings"], default=None)
    staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
    duration: Optional[DefNoteValue] = json_field(["duration"], default=None)
    stem_direction: Optional[DefStemDirection] = json_field(
        ["stemDirection"], default=None
    )
    slurs: Optional[list[Slur]] = json_field(["slurs"], default=None)
    measure: Optional[bool] = json_field(["measure"], default=None)
    rest: Optional[Rest] = json_field(["rest"], default=None)


DefStaffSymbol: TypeAlias = Literal["bracket", "brace", "none"]
DefIntegerUnsigned: TypeAlias = int
DefStaffLabel: TypeAlias = str
DefMeasureNumber: TypeAlias = int


@dataclass
class DefNoteValueQuantity(JSONWizard):
    # required fields:
    duration: DefNoteValue = json_field(["duration"])
    multiple: DefPositiveInteger = json_field(["multiple"])
    # optional fields:


DefStaffLabelref: TypeAlias = str
DefVoiceName: TypeAlias = str


@dataclass
class DefSystemLayoutContentChoice1(JSONWizard):
    @dataclass
    class Source(JSONWizard):
        # required fields:
        part: DefId = json_field(["part"])
        # optional fields:
        voice: Optional[DefVoiceName] = json_field(["voice"], default=None)
        staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
        stem: Optional[DefStemDirection] = json_field(["stem"], default=None)
        label: Optional[DefStaffLabel] = json_field(["label"], default=None)
        labelref: Optional[DefStaffLabelref] = json_field(["labelref"], default=None)

    # required fields:
    sources: list[Source] = json_field(["sources"])
    type: Literal["staff"] = json_field(["type"])
    # optional fields:
    symbol: Optional[DefStaffSymbol] = json_field(["symbol"], default=None)
    label: Optional[DefStaffLabel] = json_field(["label"], default=None)
    labelref: Optional[DefStaffLabelref] = json_field(["labelref"], default=None)


@dataclass
class DefBeamList(JSONWizard):
    @dataclass
    class Hook(JSONWizard):
        # required fields:
        direction: Literal["left", "right"] = json_field(["direction"])
        event: DefId = json_field(["event"])
        # optional fields:

    # required fields:
    events: list[DefId] = json_field(["events"])
    # optional fields:
    inner: Optional["DefBeamList"] = json_field(["inner"], default=None)
    hooks: Optional[list[Hook]] = json_field(["hooks"], default=None)


DefSmuflGlyph: TypeAlias = str
DefTupletDisplaySetting: TypeAlias = Literal["none", "inner", "both"]


@dataclass
class DefSystemLayoutContentChoice0(JSONWizard):
    # required fields:
    type: Literal["group"] = json_field(["type"])
    content: "DefSystemLayoutContent" = json_field(["content"])
    # optional fields:
    symbol: Optional[DefStaffSymbol] = json_field(["symbol"], default=None)
    label: Optional[DefStaffLabel] = json_field(["label"], default=None)


DefSystemLayoutContent: TypeAlias = list[
    Union[DefSystemLayoutContentChoice0, DefSystemLayoutContentChoice1]
]
DefColor: TypeAlias = str


@dataclass
class Top(JSONWizard):
    @dataclass
    class Layout(JSONWizard):
        # required fields:
        content: DefSystemLayoutContent = json_field(["content"])
        id: DefId = json_field(["id"])
        # optional fields:

    @dataclass
    class Global(JSONWizard):
        @dataclass
        class Style(JSONWizard):
            # required fields:
            selector: str = json_field(["selector"])
            # optional fields:
            color: Optional[DefColor] = json_field(["color"], default=None)

        @dataclass
        class Measure(JSONWizard):
            @dataclass
            class Barline(JSONWizard):
                # required fields:
                type: Literal[
                    "regular",
                    "dotted",
                    "dashed",
                    "heavy",
                    "light-light",
                    "light-heavy",
                    "heavy-light",
                    "heavy-heavy",
                    "tick",
                    "short",
                    "none",
                ] = json_field(["type"])
                # optional fields:

            @dataclass
            class Jump(JSONWizard):
                # required fields:
                type: Literal["dsalfine", "segno"] = json_field(["type"])
                location: DefMeasureLocation = json_field(["location"])
                # optional fields:

            @dataclass
            class RepeatStart(JSONWizard):
                # required fields:
                # optional fields:
                pass

            @dataclass
            class Ending(JSONWizard):
                # required fields:
                duration: int = json_field(["duration"])
                # optional fields:
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)
                open: Optional[bool] = json_field(["open"], default=None)
                color: Optional[DefColor] = json_field(["color"], default=None)
                numbers: Optional[list[int]] = json_field(["numbers"], default=None)

            @dataclass
            class Segno(JSONWizard):
                # required fields:
                location: DefMeasureLocation = json_field(["location"])
                # optional fields:
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)
                glyph: Optional[DefSmuflGlyph] = json_field(["glyph"], default=None)
                color: Optional[DefColor] = json_field(["color"], default=None)

            @dataclass
            class Tempo(JSONWizard):
                # required fields:
                value: DefNoteValue = json_field(["value"])
                bpm: int = json_field(["bpm"])
                # optional fields:
                location: Optional[DefMeasureLocation] = json_field(
                    ["location"], default=None
                )

            @dataclass
            class RepeatEnd(JSONWizard):
                # required fields:
                # optional fields:
                times: Optional[int] = json_field(["times"], default=None)

            @dataclass
            class Time(JSONWizard):
                # required fields:
                count: DefPositiveInteger = json_field(["count"])
                unit: Literal[1, 2, 4, 8, 16, 32, 64, 128] = json_field(["unit"])
                # optional fields:

            @dataclass
            class Fine(JSONWizard):
                # required fields:
                location: DefMeasureLocation = json_field(["location"])
                # optional fields:
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)
                color: Optional[DefColor] = json_field(["color"], default=None)

            @dataclass
            class Key(JSONWizard):
                # required fields:
                fifths: int = json_field(["fifths"])
                # optional fields:
                color: Optional[DefColor] = json_field(["color"], default=None)
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)

            # required fields:
            # optional fields:
            number: Optional[DefMeasureNumber] = json_field(["number"], default=None)
            jump: Optional[Jump] = json_field(["jump"], default=None)
            fine: Optional[Fine] = json_field(["fine"], default=None)
            segno: Optional[Segno] = json_field(["segno"], default=None)
            barline: Optional[Barline] = json_field(["barline"], default=None)
            tempos: Optional[list[Tempo]] = json_field(["tempos"], default=None)
            repeat_start: Optional[RepeatStart] = json_field(
                ["repeatStart"], default=None
            )
            repeat_end: Optional[RepeatEnd] = json_field(["repeatEnd"], default=None)
            time: Optional[Time] = json_field(["time"], default=None)
            index: Optional[DefMeasureNumber] = json_field(["index"], default=None)
            key: Optional[Key] = json_field(["key"], default=None)
            ending: Optional[Ending] = json_field(["ending"], default=None)

        # required fields:
        measures: list[Measure] = json_field(["measures"])
        # optional fields:
        styles: Optional[list[Style]] = json_field(["styles"], default=None)

    @dataclass
    class Part(JSONWizard):
        @dataclass
        class Measure(JSONWizard):
            @dataclass
            class Sequence(JSONWizard):
                @dataclass
                class ContentChoice5(JSONWizard):
                    # required fields:
                    value: str = json_field(["value"])
                    type: Literal["dynamic"] = json_field(["type"])
                    # optional fields:
                    glyph: Optional[DefSmuflGlyph] = json_field(["glyph"], default=None)

                @dataclass
                class ContentChoice1(JSONWizard):
                    # required fields:
                    type: Literal["grace"] = json_field(["type"])
                    content: list[DefEvent] = json_field(["content"])
                    # optional fields:
                    grace_type: Optional[
                        Literal["makeTime", "stealFollowing", "stealPrevious"]
                    ] = json_field(["graceType"], default=None)
                    slash: Optional[bool] = json_field(["slash"], default=None)
                    class_: Optional[DefStyleClass] = json_field(
                        ["class"], default=None
                    )
                    color: Optional[DefColor] = json_field(["color"], default=None)

                @dataclass
                class ContentChoice2(JSONWizard):
                    # required fields:
                    inner: DefNoteValueQuantity = json_field(["inner"])
                    type: Literal["tuplet"] = json_field(["type"])
                    outer: DefNoteValueQuantity = json_field(["outer"])
                    content: list[DefEvent] = json_field(["content"])
                    # optional fields:
                    show_value: Optional[DefTupletDisplaySetting] = json_field(
                        ["showValue"], default=None
                    )
                    show_number: Optional[DefTupletDisplaySetting] = json_field(
                        ["showNumber"], default=None
                    )
                    staff: Optional[DefStaffNumber] = json_field(
                        ["staff"], default=None
                    )
                    orient: Optional[DefOrientation] = json_field(
                        ["orient"], default=None
                    )
                    bracket: Optional[Literal["yes", "no", "auto"]] = json_field(
                        ["bracket"], default=None
                    )

                @dataclass
                class ContentChoice3(JSONWizard):
                    # required fields:
                    type: Literal["octave-shift"] = json_field(["type"])
                    end: DefMeasureLocation = json_field(["end"])
                    value: int = json_field(["value"])
                    # optional fields:
                    staff: Optional[DefStaffNumber] = json_field(
                        ["staff"], default=None
                    )
                    orient: Optional[DefOrientation] = json_field(
                        ["orient"], default=None
                    )

                @dataclass
                class ContentChoice4(JSONWizard):
                    # required fields:
                    duration: DefNoteValueQuantity = json_field(["duration"])
                    type: Literal["space"] = json_field(["type"])
                    # optional fields:

                # required fields:
                content: list[
                    Union[
                        DefEvent,
                        ContentChoice1,
                        ContentChoice2,
                        ContentChoice3,
                        ContentChoice4,
                        ContentChoice5,
                    ]
                ] = json_field(["content"])
                # optional fields:
                voice: Optional[DefVoiceName] = json_field(["voice"], default=None)
                staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
                orient: Optional[DefOrientation] = json_field(["orient"], default=None)

            @dataclass
            class Clef(JSONWizard):
                @dataclass
                class Clef(JSONWizard):
                    # required fields:
                    sign: Literal["C", "F", "G"] = json_field(["sign"])
                    staff_position: DefStaffPosition = json_field(["staffPosition"])
                    # optional fields:
                    class_: Optional[DefStyleClass] = json_field(
                        ["class"], default=None
                    )
                    color: Optional[str] = json_field(["color"], default=None)
                    glyph: Optional[DefSmuflGlyph] = json_field(["glyph"], default=None)
                    octave: Optional[int] = json_field(["octave"], default=None)

                @dataclass
                class Position(JSONWizard):
                    # required fields:
                    fraction: list[DefIntegerUnsigned] = json_field(["fraction"])
                    # optional fields:
                    grace_index: Optional[DefIntegerUnsigned] = json_field(
                        ["graceIndex"], default=None
                    )

                # required fields:
                clef: Clef = json_field(["clef"])
                # optional fields:
                position: Optional[Position] = json_field(["position"], default=None)

            # required fields:
            sequences: list[Sequence] = json_field(["sequences"])
            # optional fields:
            clefs: Optional[list[Clef]] = json_field(["clefs"], default=None)
            beams: Optional[DefBeamList] = json_field(["beams"], default=None)

        # required fields:
        # optional fields:
        short_name: Optional[str] = json_field(["shortName"], default=None)
        id: Optional[DefId] = json_field(["id"], default=None)
        smufl_font: Optional[DefSmuflFont] = json_field(["smuflFont"], default=None)
        measures: Optional[list[Measure]] = json_field(["measures"], default=None)
        name: Optional[str] = json_field(["name"], default=None)
        staves: Optional[int] = json_field(["staves"], default=None)

    @dataclass
    class Mnx(JSONWizard):
        # required fields:
        version: int = json_field(["version"])
        # optional fields:

    @dataclass
    class Score(JSONWizard):
        @dataclass
        class MultimeasureRest(JSONWizard):
            # required fields:
            start: DefMeasureNumber = json_field(["start"])
            duration: int = json_field(["duration"])
            # optional fields:
            label: Optional[str] = json_field(["label"], default=None)

        @dataclass
        class Page(JSONWizard):
            @dataclass
            class System(JSONWizard):
                @dataclass
                class LayoutChange(JSONWizard):
                    # required fields:
                    layout: DefId = json_field(["layout"])
                    location: DefMeasureLocation = json_field(["location"])
                    # optional fields:

                # required fields:
                measure: DefMeasureNumber = json_field(["measure"])
                # optional fields:
                layout: Optional[DefId] = json_field(["layout"], default=None)
                layout_changes: Optional[list[LayoutChange]] = json_field(
                    ["layoutChanges"], default=None
                )

            # required fields:
            systems: list[System] = json_field(["systems"])
            # optional fields:
            layout: Optional[DefId] = json_field(["layout"], default=None)

        # required fields:
        name: str = json_field(["name"])
        # optional fields:
        layout: Optional[DefId] = json_field(["layout"], default=None)
        multimeasure_rests: Optional[list[MultimeasureRest]] = json_field(
            ["multimeasureRests"], default=None
        )
        pages: Optional[list[Page]] = json_field(["pages"], default=None)

    # required fields:
    parts: list[Part] = json_field(["parts"])
    mnx: Mnx = json_field(["mnx"])
    global_: Global = json_field(["global"])
    # optional fields:
    layouts: Optional[list[Layout]] = json_field(["layouts"], default=None)
    scores: Optional[list[Score]] = json_field(["scores"], default=None)
