from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import *
from dataclass_wizard import JSONWizard, json_field  # type: ignore

DefVoiceName: TypeAlias = str
DefStaffSymbol: TypeAlias = Literal["bracket", "brace", "none"]
DefStaffLabel: TypeAlias = str
DefStaffLabelref: TypeAlias = str
DefStaffNumber: TypeAlias = int
DefStemDirection: TypeAlias = Literal["up", "down"]
DefId: TypeAlias = str


@dataclass
class DefSystemLayoutContentChoice1(JSONWizard):
    class _(JSONWizard.Meta):
        tag = "staff"

    @dataclass
    class Source(JSONWizard):
        # required fields:
        part: DefId = json_field(["part"])
        # optional fields:
        stem: Optional[DefStemDirection] = json_field(["stem"], default=None)
        staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
        label: Optional[DefStaffLabel] = json_field(["label"], default=None)
        voice: Optional[DefVoiceName] = json_field(["voice"], default=None)
        labelref: Optional[DefStaffLabelref] = json_field(["labelref"], default=None)

    # required fields:
    sources: list[Source] = json_field(["sources"])
    type: Literal["staff"] = json_field(["type"])
    # optional fields:
    labelref: Optional[DefStaffLabelref] = json_field(["labelref"], default=None)
    label: Optional[DefStaffLabel] = json_field(["label"], default=None)
    symbol: Optional[DefStaffSymbol] = json_field(["symbol"], default=None)


@dataclass
class DefSystemLayoutContentChoice0(JSONWizard):
    class _(JSONWizard.Meta):
        tag = "group"

    # required fields:
    type: Literal["group"] = json_field(["type"])
    content: "DefSystemLayoutContent" = json_field(["content"])
    # optional fields:
    label: Optional[DefStaffLabel] = json_field(["label"], default=None)
    symbol: Optional[DefStaffSymbol] = json_field(["symbol"], default=None)


DefSystemLayoutContent: TypeAlias = list[
    # Union[DefSystemLayoutContentChoice0, DefSystemLayoutContentChoice1]
    dict
]
DefColor: TypeAlias = str
DefStaffPosition: TypeAlias = int
DefSmuflGlyph: TypeAlias = str
DefSlurTieEndLocation: TypeAlias = str
DefStyleClass: TypeAlias = str
DefSmuflFont: TypeAlias = str
DefOrientation: TypeAlias = str
DefUpOrDown: TypeAlias = Literal["up", "down"]
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


DefSlurSide: TypeAlias = Literal["up", "down"]


@dataclass
class DefEvent(JSONWizard):
    class _(JSONWizard.Meta):
        tag = "event"

    @dataclass
    class Slur(JSONWizard):
        # required fields:
        # optional fields:
        target: Optional[DefId] = json_field(["target"], default=None)
        line_type: Optional[str] = json_field(["lineType"], default=None)
        side_end: Optional[DefSlurSide] = json_field(["sideEnd"], default=None)
        start_note: Optional[DefId] = json_field(["startNote"], default=None)
        end_note: Optional[DefId] = json_field(["endNote"], default=None)
        location: Optional[DefSlurTieEndLocation] = json_field(
            ["location"], default=None
        )
        side: Optional[DefSlurSide] = json_field(["side"], default=None)

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
        class Perform(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Pitch(JSONWizard):
            # required fields:
            step: Literal["A", "B", "C", "D", "E", "F", "G"] = json_field(["step"])
            octave: int = json_field(["octave"])
            # optional fields:
            alter: Optional[int] = json_field(["alter"], default=None)

        @dataclass
        class AccidentalDisplay(JSONWizard):
            # required fields:
            show: bool = json_field(["show"])
            # optional fields:
            editorial: Optional[bool] = json_field(["editorial"], default=None)
            cautionary: Optional[bool] = json_field(["cautionary"], default=None)

        # required fields:
        pitch: Pitch = json_field(["pitch"])
        # optional fields:
        class_: Optional[DefStyleClass] = json_field(["class"], default=None)
        perform: Optional[Perform] = json_field(["perform"], default=None)
        tie: Optional[Tie] = json_field(["tie"], default=None)
        staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
        id: Optional[DefId] = json_field(["id"], default=None)
        accidental_display: Optional[AccidentalDisplay] = json_field(
            ["accidentalDisplay"], default=None
        )
        smufl_font: Optional[DefSmuflFont] = json_field(["smuflFont"], default=None)

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
        class Staccatissimo(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class StrongAccent(JSONWizard):
            # required fields:
            # optional fields:
            pointing: Optional[DefUpOrDown] = json_field(["pointing"], default=None)

        @dataclass
        class SoftAccent(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Tremolo(JSONWizard):
            # required fields:
            marks: DefPositiveInteger = json_field(["marks"])
            # optional fields:

        @dataclass
        class Tenuto(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Stress(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Accent(JSONWizard):
            # required fields:
            # optional fields:
            pointing: Optional[DefUpOrDown] = json_field(["pointing"], default=None)

        @dataclass
        class Staccato(JSONWizard):
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
        class Spiccato(JSONWizard):
            # required fields:
            # optional fields:
            pass

        # required fields:
        # optional fields:
        soft_accent: Optional[SoftAccent] = json_field(["softAccent"], default=None)
        staccato: Optional[Staccato] = json_field(["staccato"], default=None)
        tenuto: Optional[Tenuto] = json_field(["tenuto"], default=None)
        breath: Optional[Breath] = json_field(["breath"], default=None)
        unstress: Optional[Unstress] = json_field(["unstress"], default=None)
        strong_accent: Optional[StrongAccent] = json_field(
            ["strongAccent"], default=None
        )
        accent: Optional[Accent] = json_field(["accent"], default=None)
        stress: Optional[Stress] = json_field(["stress"], default=None)
        tremolo: Optional[Tremolo] = json_field(["tremolo"], default=None)
        staccatissimo: Optional[Staccatissimo] = json_field(
            ["staccatissimo"], default=None
        )
        spiccato: Optional[Spiccato] = json_field(["spiccato"], default=None)

    # required fields:
    type: Literal["event"] = json_field(["type"])
    # optional fields:
    staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
    stem_direction: Optional[DefStemDirection] = json_field(
        ["stemDirection"], default=None
    )
    duration: Optional[DefNoteValue] = json_field(["duration"], default=None)
    smufl_font: Optional[DefSmuflFont] = json_field(["smuflFont"], default=None)
    measure: Optional[bool] = json_field(["measure"], default=None)
    rest: Optional[Rest] = json_field(["rest"], default=None)
    orient: Optional[DefOrientation] = json_field(["orient"], default=None)
    id: Optional[DefId] = json_field(["id"], default=None)
    markings: Optional[Markings] = json_field(["markings"], default=None)
    notes: Optional[list[Note]] = json_field(["notes"], default=None)
    slurs: Optional[list[Slur]] = json_field(["slurs"], default=None)


DefTupletDisplaySetting: TypeAlias = Literal["none", "inner", "both"]
DefBeamList: TypeAlias = list['DefBeam']


@dataclass
class DefBeam(JSONWizard):
    @dataclass
    class Hook(JSONWizard):
        # required fields:
        direction: Literal["left", "right"] = json_field(["direction"])
        event: DefId = json_field(["event"])
        # optional fields:

    # required fields:
    events: list[DefId] = json_field(["events"])
    # optional fields:
    hooks: Optional[list[Hook]] = json_field(["hooks"], default=None)
    # inner: Optional[DefBeamList] = json_field(["inner"], default=None)
    inner: Optional[dict] = json_field(["inner"], default=None)


@dataclass
class DefNoteValueQuantity(JSONWizard):
    # required fields:
    multiple: DefPositiveInteger = json_field(["multiple"])
    duration: DefNoteValue = json_field(["duration"])
    # optional fields:


DefMeasureNumber: TypeAlias = int
DefMeasureLocation: TypeAlias = str
DefIntegerUnsigned: TypeAlias = int


@dataclass
class Top(JSONWizard):
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
            class Segno(JSONWizard):
                # required fields:
                location: DefMeasureLocation = json_field(["location"])
                # optional fields:
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)
                color: Optional[DefColor] = json_field(["color"], default=None)
                glyph: Optional[DefSmuflGlyph] = json_field(["glyph"], default=None)

            @dataclass
            class Barline(JSONWizard):
                class _(JSONWizard.Meta):
                    tag = "regular"

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
            class Time(JSONWizard):
                # required fields:
                unit: Literal[1, 2, 4, 8, 16, 32, 64, 128] = json_field(["unit"])
                count: DefPositiveInteger = json_field(["count"])
                # optional fields:

            @dataclass
            class Tempo(JSONWizard):
                # required fields:
                bpm: int = json_field(["bpm"])
                value: DefNoteValue = json_field(["value"])
                # optional fields:
                location: Optional[DefMeasureLocation] = json_field(
                    ["location"], default=None
                )

            @dataclass
            class Key(JSONWizard):
                # required fields:
                fifths: int = json_field(["fifths"])
                # optional fields:
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)
                color: Optional[DefColor] = json_field(["color"], default=None)

            @dataclass
            class Fine(JSONWizard):
                # required fields:
                location: DefMeasureLocation = json_field(["location"])
                # optional fields:
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)
                color: Optional[DefColor] = json_field(["color"], default=None)

            @dataclass
            class Ending(JSONWizard):
                # required fields:
                duration: int = json_field(["duration"])
                # optional fields:
                numbers: Optional[list[int]] = json_field(["numbers"], default=None)
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)
                open: Optional[bool] = json_field(["open"], default=None)
                color: Optional[DefColor] = json_field(["color"], default=None)

            @dataclass
            class RepeatStart(JSONWizard):
                # required fields:
                # optional fields:
                pass

            @dataclass
            class Jump(JSONWizard):
                class _(JSONWizard.Meta):
                    tag = "dsalfine"

                # required fields:
                location: DefMeasureLocation = json_field(["location"])
                type: Literal["dsalfine", "segno"] = json_field(["type"])
                # optional fields:

            @dataclass
            class RepeatEnd(JSONWizard):
                # required fields:
                # optional fields:
                times: Optional[int] = json_field(["times"], default=None)

            # required fields:
            # optional fields:
            jump: Optional[Jump] = json_field(["jump"], default=None)
            fine: Optional[Fine] = json_field(["fine"], default=None)
            tempos: Optional[list[Tempo]] = json_field(["tempos"], default=None)
            ending: Optional[Ending] = json_field(["ending"], default=None)
            number: Optional[DefMeasureNumber] = json_field(["number"], default=None)
            barline: Optional[Barline] = json_field(["barline"], default=None)
            index: Optional[DefMeasureNumber] = json_field(["index"], default=None)
            repeat_start: Optional[RepeatStart] = json_field(
                ["repeatStart"], default=None
            )
            time: Optional[Time] = json_field(["time"], default=None)
            key: Optional[Key] = json_field(["key"], default=None)
            segno: Optional[Segno] = json_field(["segno"], default=None)
            repeat_end: Optional[RepeatEnd] = json_field(["repeatEnd"], default=None)

        # required fields:
        measures: list[Measure] = json_field(["measures"])
        # optional fields:
        styles: Optional[list[Style]] = json_field(["styles"], default=None)

    @dataclass
    class Layout(JSONWizard):
        # required fields:
        content: DefSystemLayoutContent = json_field(["content"])
        id: DefId = json_field(["id"])
        # optional fields:

    @dataclass
    class Part(JSONWizard):
        @dataclass
        class Measure(JSONWizard):
            @dataclass
            class Clef(JSONWizard):
                @dataclass
                class Position(JSONWizard):
                    # required fields:
                    fraction: list[DefIntegerUnsigned] = json_field(["fraction"])
                    # optional fields:
                    grace_index: Optional[DefIntegerUnsigned] = json_field(
                        ["graceIndex"], default=None
                    )

                @dataclass
                class Clef(JSONWizard):
                    # required fields:
                    staff_position: DefStaffPosition = json_field(["staffPosition"])
                    sign: Literal["C", "F", "G"] = json_field(["sign"])
                    # optional fields:
                    color: Optional[str] = json_field(["color"], default=None)
                    glyph: Optional[DefSmuflGlyph] = json_field(["glyph"], default=None)
                    class_: Optional[DefStyleClass] = json_field(
                        ["class"], default=None
                    )
                    octave: Optional[int] = json_field(["octave"], default=None)

                # required fields:
                clef: Clef = json_field(["clef"])
                # optional fields:
                position: Optional[Position] = json_field(["position"], default=None)

            @dataclass
            class Sequence(JSONWizard):
                @dataclass
                class ContentChoice5(JSONWizard):
                    class _(JSONWizard.Meta):
                        tag = "dynamic"

                    # required fields:
                    type: Literal["dynamic"] = json_field(["type"])
                    value: str = json_field(["value"])
                    # optional fields:
                    glyph: Optional[DefSmuflGlyph] = json_field(["glyph"], default=None)

                @dataclass
                class ContentChoice2(JSONWizard):
                    class _(JSONWizard.Meta):
                        tag = "tuplet"

                    # required fields:
                    inner: DefNoteValueQuantity = json_field(["inner"])
                    type: Literal["tuplet"] = json_field(["type"])
                    outer: DefNoteValueQuantity = json_field(["outer"])
                    content: list[DefEvent] = json_field(["content"])
                    # optional fields:
                    staff: Optional[DefStaffNumber] = json_field(
                        ["staff"], default=None
                    )
                    orient: Optional[DefOrientation] = json_field(
                        ["orient"], default=None
                    )
                    bracket: Optional[Literal["yes", "no", "auto"]] = json_field(
                        ["bracket"], default=None
                    )
                    show_number: Optional[DefTupletDisplaySetting] = json_field(
                        ["showNumber"], default=None
                    )
                    show_value: Optional[DefTupletDisplaySetting] = json_field(
                        ["showValue"], default=None
                    )

                @dataclass
                class ContentChoice3(JSONWizard):
                    class _(JSONWizard.Meta):
                        tag = "octave-shift"

                    # required fields:
                    type: Literal["octave-shift"] = json_field(["type"])
                    value: int = json_field(["value"])
                    end: DefMeasureLocation = json_field(["end"])
                    # optional fields:
                    orient: Optional[DefOrientation] = json_field(
                        ["orient"], default=None
                    )
                    staff: Optional[DefStaffNumber] = json_field(
                        ["staff"], default=None
                    )

                @dataclass
                class ContentChoice4(JSONWizard):
                    class _(JSONWizard.Meta):
                        tag = "space"

                    # required fields:
                    duration: DefNoteValueQuantity = json_field(["duration"])
                    type: Literal["space"] = json_field(["type"])
                    # optional fields:

                @dataclass
                class ContentChoice1(JSONWizard):
                    class _(JSONWizard.Meta):
                        tag = "grace"

                    # required fields:
                    type: Literal["grace"] = json_field(["type"])
                    content: list[DefEvent] = json_field(["content"])
                    # optional fields:
                    slash: Optional[bool] = json_field(["slash"], default=None)
                    color: Optional[DefColor] = json_field(["color"], default=None)
                    class_: Optional[DefStyleClass] = json_field(
                        ["class"], default=None
                    )
                    grace_type: Optional[
                        Literal["makeTime", "stealFollowing", "stealPrevious"]
                    ] = json_field(["graceType"], default=None)

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
                staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
                voice: Optional[DefVoiceName] = json_field(["voice"], default=None)
                orient: Optional[DefOrientation] = json_field(["orient"], default=None)

            # required fields:
            sequences: list[Sequence] = json_field(["sequences"])
            # optional fields:
            beams: Optional[DefBeamList] = json_field(["beams"], default=None)
            clefs: Optional[list[Clef]] = json_field(["clefs"], default=None)

        # required fields:
        # optional fields:
        smufl_font: Optional[DefSmuflFont] = json_field(["smuflFont"], default=None)
        id: Optional[DefId] = json_field(["id"], default=None)
        measures: Optional[list[Measure]] = json_field(["measures"], default=None)
        name: Optional[str] = json_field(["name"], default=None)
        short_name: Optional[str] = json_field(["shortName"], default=None)
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
                layout_changes: Optional[list[LayoutChange]] = json_field(
                    ["layoutChanges"], default=None
                )
                layout: Optional[DefId] = json_field(["layout"], default=None)

            # required fields:
            systems: list[System] = json_field(["systems"])
            # optional fields:
            layout: Optional[DefId] = json_field(["layout"], default=None)

        # required fields:
        name: str = json_field(["name"])
        # optional fields:
        multimeasure_rests: Optional[list[MultimeasureRest]] = json_field(
            ["multimeasureRests"], default=None
        )
        layout: Optional[DefId] = json_field(["layout"], default=None)
        pages: Optional[list[Page]] = json_field(["pages"], default=None)

    class _(JSONWizard.Meta):
        tag_key = "type"
        auto_assign_tags = True

    # required fields:
    global_: Global = json_field(["global"])
    mnx: Mnx = json_field(["mnx"])
    parts: list[Part] = json_field(["parts"])
    # optional fields:
    scores: Optional[list[Score]] = json_field(["scores"], default=None)
    layouts: Optional[list[Layout]] = json_field(["layouts"], default=None)
