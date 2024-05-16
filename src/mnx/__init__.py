from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import *
from dataclass_wizard import JSONWizard, json_field  # type: ignore

DefVoiceName: TypeAlias = str
DefStaffSymbol: TypeAlias = Literal["bracket", "brace", "none"]
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


@dataclass
class DefNoteValueQuantity(JSONWizard):
    # required fields:
    duration: DefNoteValue = json_field(["duration"])
    multiple: DefPositiveInteger = json_field(["multiple"])
    # optional fields:


DefUpOrDown: TypeAlias = Literal["up", "down"]
DefStaffPosition: TypeAlias = int
DefId: TypeAlias = str
DefColor: TypeAlias = str
DefSlurTieEndLocation: TypeAlias = str
DefStemDirection: TypeAlias = Literal["up", "down"]
DefSlurSide: TypeAlias = Literal["up", "down"]
DefStyleClass: TypeAlias = str
DefOrientation: TypeAlias = str
DefStaffNumber: TypeAlias = int
DefSmuflFont: TypeAlias = str


@dataclass
class DefEvent(JSONWizard):
    class _(JSONWizard.Meta):
        tag_key = "event"

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
        class Breath(JSONWizard):
            # required fields:
            # optional fields:
            symbol: Optional[str] = json_field(["symbol"], default=None)

        @dataclass
        class Staccato(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Tremolo(JSONWizard):
            # required fields:
            marks: DefPositiveInteger = json_field(["marks"])
            # optional fields:

        @dataclass
        class Unstress(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Stress(JSONWizard):
            # required fields:
            # optional fields:
            pass

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
        class Accent(JSONWizard):
            # required fields:
            # optional fields:
            pointing: Optional[DefUpOrDown] = json_field(["pointing"], default=None)

        @dataclass
        class StrongAccent(JSONWizard):
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

        # required fields:
        # optional fields:
        unstress: Optional[Unstress] = json_field(["unstress"], default=None)
        staccato: Optional[Staccato] = json_field(["staccato"], default=None)
        accent: Optional[Accent] = json_field(["accent"], default=None)
        strong_accent: Optional[StrongAccent] = json_field(
            ["strongAccent"], default=None
        )
        stress: Optional[Stress] = json_field(["stress"], default=None)
        staccatissimo: Optional[Staccatissimo] = json_field(
            ["staccatissimo"], default=None
        )
        spiccato: Optional[Spiccato] = json_field(["spiccato"], default=None)
        soft_accent: Optional[SoftAccent] = json_field(["softAccent"], default=None)
        breath: Optional[Breath] = json_field(["breath"], default=None)
        tremolo: Optional[Tremolo] = json_field(["tremolo"], default=None)
        tenuto: Optional[Tenuto] = json_field(["tenuto"], default=None)

    @dataclass
    class Note(JSONWizard):
        @dataclass
        class Tie(JSONWizard):
            # required fields:
            # optional fields:
            target: Optional[DefId] = json_field(["target"], default=None)
            location: Optional[DefSlurTieEndLocation] = json_field(
                ["location"], default=None
            )

        @dataclass
        class Pitch(JSONWizard):
            # required fields:
            octave: int = json_field(["octave"])
            step: Literal["A", "B", "C", "D", "E", "F", "G"] = json_field(["step"])
            # optional fields:
            alter: Optional[int] = json_field(["alter"], default=None)

        @dataclass
        class AccidentalDisplay(JSONWizard):
            # required fields:
            show: bool = json_field(["show"])
            # optional fields:
            editorial: Optional[bool] = json_field(["editorial"], default=None)
            cautionary: Optional[bool] = json_field(["cautionary"], default=None)

        @dataclass
        class Perform(JSONWizard):
            # required fields:
            # optional fields:
            pass

        # required fields:
        pitch: Pitch = json_field(["pitch"])
        # optional fields:
        tie: Optional[Tie] = json_field(["tie"], default=None)
        id: Optional[DefId] = json_field(["id"], default=None)
        accidental_display: Optional[AccidentalDisplay] = json_field(
            ["accidentalDisplay"], default=None
        )
        perform: Optional[Perform] = json_field(["perform"], default=None)
        class_: Optional[DefStyleClass] = json_field(["class"], default=None)
        staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
        smufl_font: Optional[DefSmuflFont] = json_field(["smuflFont"], default=None)

    @dataclass
    class Slur(JSONWizard):
        # required fields:
        # optional fields:
        end_note: Optional[DefId] = json_field(["endNote"], default=None)
        target: Optional[DefId] = json_field(["target"], default=None)
        side_end: Optional[DefSlurSide] = json_field(["sideEnd"], default=None)
        line_type: Optional[str] = json_field(["lineType"], default=None)
        side: Optional[DefSlurSide] = json_field(["side"], default=None)
        start_note: Optional[DefId] = json_field(["startNote"], default=None)
        location: Optional[DefSlurTieEndLocation] = json_field(
            ["location"], default=None
        )

    # required fields:
    type: Literal["event"] = json_field(["type"])
    # optional fields:
    measure: Optional[bool] = json_field(["measure"], default=None)
    stem_direction: Optional[DefStemDirection] = json_field(
        ["stemDirection"], default=None
    )
    id: Optional[DefId] = json_field(["id"], default=None)
    orient: Optional[DefOrientation] = json_field(["orient"], default=None)
    markings: Optional[Markings] = json_field(["markings"], default=None)
    smufl_font: Optional[DefSmuflFont] = json_field(["smuflFont"], default=None)
    slurs: Optional[list[Slur]] = json_field(["slurs"], default=None)
    rest: Optional[Rest] = json_field(["rest"], default=None)
    notes: Optional[list[Note]] = json_field(["notes"], default=None)
    duration: Optional[DefNoteValue] = json_field(["duration"], default=None)
    staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)


DefIntegerUnsigned: TypeAlias = int
DefTupletDisplaySetting: TypeAlias = Literal["none", "inner", "both"]


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
    inner: Optional['DefBeamList'] = json_field(["inner"], default=None)
    hooks: Optional[list[Hook]] = json_field(["hooks"], default=None)


DefStaffLabelref: TypeAlias = str
DefStaffLabel: TypeAlias = str

DefSystemLayoutContent: TypeAlias = list[
    Union['DefSystemLayoutContentChoice0', 'DefSystemLayoutContentChoice1']
]

@dataclass
class DefSystemLayoutContentChoice1(JSONWizard):
    class _(JSONWizard.Meta):
        tag_key = "staff"

    @dataclass
    class Source(JSONWizard):
        # required fields:
        part: DefId = json_field(["part"])
        # optional fields:
        labelref: Optional[DefStaffLabelref] = json_field(["labelref"], default=None)
        staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
        stem: Optional[DefStemDirection] = json_field(["stem"], default=None)
        label: Optional[DefStaffLabel] = json_field(["label"], default=None)
        voice: Optional[DefVoiceName] = json_field(["voice"], default=None)

    # required fields:
    type: Literal["staff"] = json_field(["type"])
    sources: list[Source] = json_field(["sources"])
    # optional fields:
    label: Optional[DefStaffLabel] = json_field(["label"], default=None)
    labelref: Optional[DefStaffLabelref] = json_field(["labelref"], default=None)
    symbol: Optional[DefStaffSymbol] = json_field(["symbol"], default=None)


DefSmuflGlyph: TypeAlias = str


@dataclass
class DefSystemLayoutContentChoice0(JSONWizard):
    class _(JSONWizard.Meta):
        tag_key = "group"

    # required fields:
    content: DefSystemLayoutContent = json_field(["content"])
    type: Literal["group"] = json_field(["type"])
    # optional fields:
    label: Optional[DefStaffLabel] = json_field(["label"], default=None)
    symbol: Optional[DefStaffSymbol] = json_field(["symbol"], default=None)


DefMeasureNumber: TypeAlias = int
DefMeasureLocation: TypeAlias = str


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
                glyph: Optional[DefSmuflGlyph] = json_field(["glyph"], default=None)
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)
                color: Optional[DefColor] = json_field(["color"], default=None)

            @dataclass
            class RepeatEnd(JSONWizard):
                # required fields:
                # optional fields:
                times: Optional[int] = json_field(["times"], default=None)

            @dataclass
            class Jump(JSONWizard):
                class _(JSONWizard.Meta):
                    tag_key = "dsalfine"

                # required fields:
                location: DefMeasureLocation = json_field(["location"])
                type: Literal["dsalfine", "segno"] = json_field(["type"])
                # optional fields:

            @dataclass
            class Key(JSONWizard):
                # required fields:
                fifths: int = json_field(["fifths"])
                # optional fields:
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)
                color: Optional[DefColor] = json_field(["color"], default=None)

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
            class Fine(JSONWizard):
                # required fields:
                location: DefMeasureLocation = json_field(["location"])
                # optional fields:
                color: Optional[DefColor] = json_field(["color"], default=None)
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)

            @dataclass
            class Ending(JSONWizard):
                # required fields:
                duration: int = json_field(["duration"])
                # optional fields:
                color: Optional[DefColor] = json_field(["color"], default=None)
                open: Optional[bool] = json_field(["open"], default=None)
                numbers: Optional[list[int]] = json_field(["numbers"], default=None)
                class_: Optional[DefStyleClass] = json_field(["class"], default=None)

            @dataclass
            class RepeatStart(JSONWizard):
                # required fields:
                # optional fields:
                pass

            @dataclass
            class Time(JSONWizard):
                # required fields:
                unit: Literal[1, 2, 4, 8, 16, 32, 64, 128] = json_field(["unit"])
                count: DefPositiveInteger = json_field(["count"])
                # optional fields:

            @dataclass
            class Barline(JSONWizard):
                class _(JSONWizard.Meta):
                    tag_key = "regular"

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

            # required fields:
            # optional fields:
            repeat_end: Optional[RepeatEnd] = json_field(["repeatEnd"], default=None)
            jump: Optional[Jump] = json_field(["jump"], default=None)
            key: Optional[Key] = json_field(["key"], default=None)
            ending: Optional[Ending] = json_field(["ending"], default=None)
            time: Optional[Time] = json_field(["time"], default=None)
            barline: Optional[Barline] = json_field(["barline"], default=None)
            number: Optional[DefMeasureNumber] = json_field(["number"], default=None)
            fine: Optional[Fine] = json_field(["fine"], default=None)
            index: Optional[DefMeasureNumber] = json_field(["index"], default=None)
            repeat_start: Optional[RepeatStart] = json_field(
                ["repeatStart"], default=None
            )
            tempos: Optional[list[Tempo]] = json_field(["tempos"], default=None)
            segno: Optional[Segno] = json_field(["segno"], default=None)

        # required fields:
        measures: list[Measure] = json_field(["measures"])
        # optional fields:
        styles: Optional[list[Style]] = json_field(["styles"], default=None)

    @dataclass
    class Mnx(JSONWizard):
        # required fields:
        version: int = json_field(["version"])
        # optional fields:

    @dataclass
    class Layout(JSONWizard):
        # required fields:
        id: DefId = json_field(["id"])
        content: DefSystemLayoutContent = json_field(["content"])
        # optional fields:

    @dataclass
    class Part(JSONWizard):
        @dataclass
        class Measure(JSONWizard):
            @dataclass
            class Sequence(JSONWizard):
                @dataclass
                class ContentChoice5(JSONWizard):
                    class _(JSONWizard.Meta):
                        tag_key = "dynamic"

                    # required fields:
                    value: str = json_field(["value"])
                    type: Literal["dynamic"] = json_field(["type"])
                    # optional fields:
                    glyph: Optional[DefSmuflGlyph] = json_field(["glyph"], default=None)

                @dataclass
                class ContentChoice2(JSONWizard):
                    class _(JSONWizard.Meta):
                        tag_key = "tuplet"

                    # required fields:
                    content: list[DefEvent] = json_field(["content"])
                    inner: DefNoteValueQuantity = json_field(["inner"])
                    outer: DefNoteValueQuantity = json_field(["outer"])
                    type: Literal["tuplet"] = json_field(["type"])
                    # optional fields:
                    staff: Optional[DefStaffNumber] = json_field(
                        ["staff"], default=None
                    )
                    bracket: Optional[Literal["yes", "no", "auto"]] = json_field(
                        ["bracket"], default=None
                    )
                    orient: Optional[DefOrientation] = json_field(
                        ["orient"], default=None
                    )
                    show_number: Optional[DefTupletDisplaySetting] = json_field(
                        ["showNumber"], default=None
                    )
                    show_value: Optional[DefTupletDisplaySetting] = json_field(
                        ["showValue"], default=None
                    )

                @dataclass
                class ContentChoice1(JSONWizard):
                    class _(JSONWizard.Meta):
                        tag_key = "grace"

                    # required fields:
                    content: list[DefEvent] = json_field(["content"])
                    type: Literal["grace"] = json_field(["type"])
                    # optional fields:
                    grace_type: Optional[
                        Literal["makeTime", "stealFollowing", "stealPrevious"]
                    ] = json_field(["graceType"], default=None)
                    slash: Optional[bool] = json_field(["slash"], default=None)
                    color: Optional[DefColor] = json_field(["color"], default=None)
                    class_: Optional[DefStyleClass] = json_field(
                        ["class"], default=None
                    )

                @dataclass
                class ContentChoice3(JSONWizard):
                    class _(JSONWizard.Meta):
                        tag_key = "octave-shift"

                    # required fields:
                    value: int = json_field(["value"])
                    end: DefMeasureLocation = json_field(["end"])
                    type: Literal["octave-shift"] = json_field(["type"])
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
                        tag_key = "space"

                    # required fields:
                    type: Literal["space"] = json_field(["type"])
                    duration: DefNoteValueQuantity = json_field(["duration"])
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
                staff: Optional[DefStaffNumber] = json_field(["staff"], default=None)
                orient: Optional[DefOrientation] = json_field(["orient"], default=None)
                voice: Optional[DefVoiceName] = json_field(["voice"], default=None)

            @dataclass
            class Clef(JSONWizard):
                @dataclass
                class Clef(JSONWizard):
                    # required fields:
                    sign: Literal["C", "F", "G"] = json_field(["sign"])
                    staff_position: DefStaffPosition = json_field(["staffPosition"])
                    # optional fields:
                    glyph: Optional[DefSmuflGlyph] = json_field(["glyph"], default=None)
                    octave: Optional[int] = json_field(["octave"], default=None)
                    color: Optional[str] = json_field(["color"], default=None)
                    class_: Optional[DefStyleClass] = json_field(
                        ["class"], default=None
                    )

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
        staves: Optional[int] = json_field(["staves"], default=None)
        name: Optional[str] = json_field(["name"], default=None)
        short_name: Optional[str] = json_field(["shortName"], default=None)
        id: Optional[DefId] = json_field(["id"], default=None)
        measures: Optional[list[Measure]] = json_field(["measures"], default=None)
        smufl_font: Optional[DefSmuflFont] = json_field(["smuflFont"], default=None)

    @dataclass
    class Score(JSONWizard):
        @dataclass
        class Page(JSONWizard):
            @dataclass
            class System(JSONWizard):
                @dataclass
                class LayoutChange(JSONWizard):
                    # required fields:
                    location: DefMeasureLocation = json_field(["location"])
                    layout: DefId = json_field(["layout"])
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

        @dataclass
        class MultimeasureRest(JSONWizard):
            # required fields:
            duration: int = json_field(["duration"])
            start: DefMeasureNumber = json_field(["start"])
            # optional fields:
            label: Optional[str] = json_field(["label"], default=None)

        # required fields:
        name: str = json_field(["name"])
        # optional fields:
        layout: Optional[DefId] = json_field(["layout"], default=None)
        multimeasure_rests: Optional[list[MultimeasureRest]] = json_field(
            ["multimeasureRests"], default=None
        )
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
