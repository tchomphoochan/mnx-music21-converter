from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import *
from dataclass_wizard import JSONWizard, json_field  # mypy: ignore

DefStaffNumber: TypeAlias = int
DefId: TypeAlias = str
DefStaffSymbol: TypeAlias = Union[Literal["bracket"], Literal["brace"], Literal["none"]]
DefStaffLabelref: TypeAlias = str
DefVoiceName: TypeAlias = str
DefStemDirection: TypeAlias = Union[Literal["up"], Literal["down"]]
DefStaffLabel: TypeAlias = str


@dataclass
class DefSystemLayoutContentChoice1(JSONWizard):
    @dataclass
    class Source(JSONWizard):
        # required fields:
        part: "DefId" = json_field(["part"])
        # optional fields:
        staff: Optional["DefStaffNumber"] = json_field(["staff"], default=None)
        labelref: Optional["DefStaffLabelref"] = json_field(["labelref"], default=None)
        stem: Optional["DefStemDirection"] = json_field(["stem"], default=None)
        label: Optional["DefStaffLabel"] = json_field(["label"], default=None)
        voice: Optional["DefVoiceName"] = json_field(["voice"], default=None)

    # required fields:
    type: Literal["staff"] = json_field(["type"])
    sources: list["Source"] = json_field(["sources"])
    # optional fields:
    symbol: Optional["DefStaffSymbol"] = json_field(["symbol"], default=None)
    labelref: Optional["DefStaffLabelref"] = json_field(["labelref"], default=None)
    label: Optional["DefStaffLabel"] = json_field(["label"], default=None)


DefMeasureNumber: TypeAlias = int
DefColor: TypeAlias = str
DefSlurSide: TypeAlias = Union[Literal["up"], Literal["down"]]
DefStyleClass: TypeAlias = str
DefStaffPosition: TypeAlias = int
DefSmuflFont: TypeAlias = str
DefPositiveInteger: TypeAlias = int


@dataclass
class DefNoteValue(JSONWizard):
    # required fields:
    base: Union[
        Literal["duplexMaxima"],
        Literal["maxima"],
        Literal["longa"],
        Literal["breve"],
        Literal["whole"],
        Literal["half"],
        Literal["quarter"],
        Literal["eighth"],
        Literal["16th"],
        Literal["32nd"],
        Literal["64th"],
        Literal["128th"],
        Literal["256th"],
        Literal["512th"],
        Literal["1024th"],
        Literal["2048th"],
        Literal["4096th"],
    ] = json_field(["base"])
    # optional fields:
    dots: Optional["DefPositiveInteger"] = json_field(["dots"], default=None)


DefOrientation: TypeAlias = str
DefSlurTieEndLocation: TypeAlias = str
DefUpOrDown: TypeAlias = Union[Literal["up"], Literal["down"]]


@dataclass
class DefEvent(JSONWizard):
    @dataclass
    class Rest(JSONWizard):
        # required fields:
        # optional fields:
        staff_position: Optional["DefStaffPosition"] = json_field(
            ["staffPosition"], default=None
        )

    @dataclass
    class Slur(JSONWizard):
        # required fields:
        # optional fields:
        end_note: Optional["DefId"] = json_field(["endNote"], default=None)
        target: Optional["DefId"] = json_field(["target"], default=None)
        side_end: Optional["DefSlurSide"] = json_field(["sideEnd"], default=None)
        line_type: Optional[str] = json_field(["lineType"], default=None)
        location: Optional["DefSlurTieEndLocation"] = json_field(
            ["location"], default=None
        )
        side: Optional["DefSlurSide"] = json_field(["side"], default=None)
        start_note: Optional["DefId"] = json_field(["startNote"], default=None)

    @dataclass
    class Note(JSONWizard):
        @dataclass
        class Tie(JSONWizard):
            # required fields:
            # optional fields:
            target: Optional["DefId"] = json_field(["target"], default=None)
            location: Optional["DefSlurTieEndLocation"] = json_field(
                ["location"], default=None
            )

        @dataclass
        class Pitch(JSONWizard):
            # required fields:
            step: Union[
                Literal["A"],
                Literal["B"],
                Literal["C"],
                Literal["D"],
                Literal["E"],
                Literal["F"],
                Literal["G"],
            ] = json_field(["step"])
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

        @dataclass
        class Perform(JSONWizard):
            # required fields:
            # optional fields:
            pass

        # required fields:
        pitch: "Pitch" = json_field(["pitch"])
        # optional fields:
        perform: Optional["Perform"] = json_field(["perform"], default=None)
        smufl_font: Optional["DefSmuflFont"] = json_field(["smuflFont"], default=None)
        class_: Optional["DefStyleClass"] = json_field(["class"], default=None)
        id: Optional["DefId"] = json_field(["id"], default=None)
        tie: Optional["Tie"] = json_field(["tie"], default=None)
        accidental_display: Optional["AccidentalDisplay"] = json_field(
            ["accidentalDisplay"], default=None
        )
        staff: Optional["DefStaffNumber"] = json_field(["staff"], default=None)

    @dataclass
    class Markings(JSONWizard):
        @dataclass
        class Tremolo(JSONWizard):
            # required fields:
            marks: "DefPositiveInteger" = json_field(["marks"])
            # optional fields:

        @dataclass
        class Unstress(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Accent(JSONWizard):
            # required fields:
            # optional fields:
            pointing: Optional["DefUpOrDown"] = json_field(["pointing"], default=None)

        @dataclass
        class Stress(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Staccato(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Spiccato(JSONWizard):
            # required fields:
            # optional fields:
            pass

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
        class Tenuto(JSONWizard):
            # required fields:
            # optional fields:
            pass

        @dataclass
        class Breath(JSONWizard):
            # required fields:
            # optional fields:
            symbol: Optional[str] = json_field(["symbol"], default=None)

        @dataclass
        class StrongAccent(JSONWizard):
            # required fields:
            # optional fields:
            pointing: Optional["DefUpOrDown"] = json_field(["pointing"], default=None)

        # required fields:
        # optional fields:
        tenuto: Optional["Tenuto"] = json_field(["tenuto"], default=None)
        tremolo: Optional["Tremolo"] = json_field(["tremolo"], default=None)
        spiccato: Optional["Spiccato"] = json_field(["spiccato"], default=None)
        staccato: Optional["Staccato"] = json_field(["staccato"], default=None)
        accent: Optional["Accent"] = json_field(["accent"], default=None)
        unstress: Optional["Unstress"] = json_field(["unstress"], default=None)
        staccatissimo: Optional["Staccatissimo"] = json_field(
            ["staccatissimo"], default=None
        )
        stress: Optional["Stress"] = json_field(["stress"], default=None)
        soft_accent: Optional["SoftAccent"] = json_field(["softAccent"], default=None)
        strong_accent: Optional["StrongAccent"] = json_field(
            ["strongAccent"], default=None
        )
        breath: Optional["Breath"] = json_field(["breath"], default=None)

    # required fields:
    type: Literal["event"] = json_field(["type"])
    # optional fields:
    rest: Optional["Rest"] = json_field(["rest"], default=None)
    markings: Optional["Markings"] = json_field(["markings"], default=None)
    duration: Optional["DefNoteValue"] = json_field(["duration"], default=None)
    orient: Optional["DefOrientation"] = json_field(["orient"], default=None)
    smufl_font: Optional["DefSmuflFont"] = json_field(["smuflFont"], default=None)
    stem_direction: Optional["DefStemDirection"] = json_field(
        ["stemDirection"], default=None
    )
    measure: Optional[bool] = json_field(["measure"], default=None)
    notes: Optional[list["Note"]] = json_field(["notes"], default=None)
    staff: Optional["DefStaffNumber"] = json_field(["staff"], default=None)
    slurs: Optional[list["Slur"]] = json_field(["slurs"], default=None)
    id: Optional["DefId"] = json_field(["id"], default=None)


@dataclass
class DefBeamList(JSONWizard):
    @dataclass
    class Hook(JSONWizard):
        # required fields:
        event: "DefId" = json_field(["event"])
        direction: Union[Literal["left"], Literal["right"]] = json_field(["direction"])
        # optional fields:

    # required fields:
    events: list["DefId"] = json_field(["events"])
    # optional fields:
    hooks: Optional[list["Hook"]] = json_field(["hooks"], default=None)
    inner: Optional["DefBeamList"] = json_field(["inner"], default=None)


@dataclass
class DefNoteValueQuantity(JSONWizard):
    # required fields:
    multiple: "DefPositiveInteger" = json_field(["multiple"])
    duration: "DefNoteValue" = json_field(["duration"])
    # optional fields:


DefSmuflGlyph: TypeAlias = str


@dataclass
class DefSystemLayoutContentChoice0(JSONWizard):
    # required fields:
    content: "DefSystemLayoutContent" = json_field(["content"])
    type: Literal["group"] = json_field(["type"])
    # optional fields:
    symbol: Optional["DefStaffSymbol"] = json_field(["symbol"], default=None)
    label: Optional["DefStaffLabel"] = json_field(["label"], default=None)


DefSystemLayoutContent: TypeAlias = list[
    Union["DefSystemLayoutContentChoice0", "DefSystemLayoutContentChoice1"]
]
DefMeasureLocation: TypeAlias = str
DefTupletDisplaySetting: TypeAlias = Union[
    Literal["none"], Literal["inner"], Literal["both"]
]
DefIntegerUnsigned: TypeAlias = int


@dataclass
class Top(JSONWizard):
    @dataclass
    class Mnx(JSONWizard):
        # required fields:
        version: int = json_field(["version"])
        # optional fields:

    @dataclass
    class Global(JSONWizard):
        @dataclass
        class Measure(JSONWizard):
            @dataclass
            class Ending(JSONWizard):
                # required fields:
                duration: int = json_field(["duration"])
                # optional fields:
                numbers: Optional[list[int]] = json_field(["numbers"], default=None)
                open: Optional[bool] = json_field(["open"], default=None)
                color: Optional["DefColor"] = json_field(["color"], default=None)
                class_: Optional["DefStyleClass"] = json_field(["class"], default=None)

            @dataclass
            class Tempo(JSONWizard):
                # required fields:
                bpm: int = json_field(["bpm"])
                value: "DefNoteValue" = json_field(["value"])
                # optional fields:
                location: Optional["DefMeasureLocation"] = json_field(
                    ["location"], default=None
                )

            @dataclass
            class Jump(JSONWizard):
                # required fields:
                type: Union[Literal["dsalfine"], Literal["segno"]] = json_field(
                    ["type"]
                )
                location: "DefMeasureLocation" = json_field(["location"])
                # optional fields:

            @dataclass
            class RepeatEnd(JSONWizard):
                # required fields:
                # optional fields:
                times: Optional[int] = json_field(["times"], default=None)

            @dataclass
            class Barline(JSONWizard):
                # required fields:
                type: Union[
                    Literal["regular"],
                    Literal["dotted"],
                    Literal["dashed"],
                    Literal["heavy"],
                    Literal["light-light"],
                    Literal["light-heavy"],
                    Literal["heavy-light"],
                    Literal["heavy-heavy"],
                    Literal["tick"],
                    Literal["short"],
                    Literal["none"],
                ] = json_field(["type"])
                # optional fields:

            @dataclass
            class Time(JSONWizard):
                # required fields:
                count: "DefPositiveInteger" = json_field(["count"])
                unit: Union[
                    Literal[1],
                    Literal[2],
                    Literal[4],
                    Literal[8],
                    Literal[16],
                    Literal[32],
                    Literal[64],
                    Literal[128],
                ] = json_field(["unit"])
                # optional fields:

            @dataclass
            class Key(JSONWizard):
                # required fields:
                fifths: int = json_field(["fifths"])
                # optional fields:
                color: Optional["DefColor"] = json_field(["color"], default=None)
                class_: Optional["DefStyleClass"] = json_field(["class"], default=None)

            @dataclass
            class RepeatStart(JSONWizard):
                # required fields:
                # optional fields:
                pass

            @dataclass
            class Fine(JSONWizard):
                # required fields:
                location: "DefMeasureLocation" = json_field(["location"])
                # optional fields:
                color: Optional["DefColor"] = json_field(["color"], default=None)
                class_: Optional["DefStyleClass"] = json_field(["class"], default=None)

            @dataclass
            class Segno(JSONWizard):
                # required fields:
                location: "DefMeasureLocation" = json_field(["location"])
                # optional fields:
                class_: Optional["DefStyleClass"] = json_field(["class"], default=None)
                glyph: Optional["DefSmuflGlyph"] = json_field(["glyph"], default=None)
                color: Optional["DefColor"] = json_field(["color"], default=None)

            # required fields:
            # optional fields:
            barline: Optional["Barline"] = json_field(["barline"], default=None)
            time: Optional["Time"] = json_field(["time"], default=None)
            repeat_end: Optional["RepeatEnd"] = json_field(["repeatEnd"], default=None)
            key: Optional["Key"] = json_field(["key"], default=None)
            tempos: Optional[list["Tempo"]] = json_field(["tempos"], default=None)
            index: Optional["DefMeasureNumber"] = json_field(["index"], default=None)
            jump: Optional["Jump"] = json_field(["jump"], default=None)
            fine: Optional["Fine"] = json_field(["fine"], default=None)
            segno: Optional["Segno"] = json_field(["segno"], default=None)
            number: Optional["DefMeasureNumber"] = json_field(["number"], default=None)
            repeat_start: Optional["RepeatStart"] = json_field(
                ["repeatStart"], default=None
            )
            ending: Optional["Ending"] = json_field(["ending"], default=None)

        @dataclass
        class Style(JSONWizard):
            # required fields:
            selector: str = json_field(["selector"])
            # optional fields:
            color: Optional["DefColor"] = json_field(["color"], default=None)

        # required fields:
        measures: list["Measure"] = json_field(["measures"])
        # optional fields:
        styles: Optional[list["Style"]] = json_field(["styles"], default=None)

    @dataclass
    class Part(JSONWizard):
        @dataclass
        class Measure(JSONWizard):
            @dataclass
            class Sequence(JSONWizard):
                @dataclass
                class ContentChoice4(JSONWizard):
                    # required fields:
                    type: Literal["space"] = json_field(["type"])
                    duration: "DefNoteValueQuantity" = json_field(["duration"])
                    # optional fields:

                @dataclass
                class ContentChoice5(JSONWizard):
                    # required fields:
                    value: str = json_field(["value"])
                    type: Literal["dynamic"] = json_field(["type"])
                    # optional fields:
                    glyph: Optional["DefSmuflGlyph"] = json_field(
                        ["glyph"], default=None
                    )

                @dataclass
                class ContentChoice3(JSONWizard):
                    # required fields:
                    value: int = json_field(["value"])
                    end: "DefMeasureLocation" = json_field(["end"])
                    type: Literal["octave-shift"] = json_field(["type"])
                    # optional fields:
                    staff: Optional["DefStaffNumber"] = json_field(
                        ["staff"], default=None
                    )
                    orient: Optional["DefOrientation"] = json_field(
                        ["orient"], default=None
                    )

                @dataclass
                class ContentChoice1(JSONWizard):
                    # required fields:
                    type: Literal["grace"] = json_field(["type"])
                    content: list["DefEvent"] = json_field(["content"])
                    # optional fields:
                    class_: Optional["DefStyleClass"] = json_field(
                        ["class"], default=None
                    )
                    slash: Optional[bool] = json_field(["slash"], default=None)
                    color: Optional["DefColor"] = json_field(["color"], default=None)
                    grace_type: Optional[
                        Union[
                            Literal["makeTime"],
                            Literal["stealFollowing"],
                            Literal["stealPrevious"],
                        ]
                    ] = json_field(["graceType"], default=None)

                @dataclass
                class ContentChoice2(JSONWizard):
                    # required fields:
                    content: list["DefEvent"] = json_field(["content"])
                    outer: "DefNoteValueQuantity" = json_field(["outer"])
                    inner: "DefNoteValueQuantity" = json_field(["inner"])
                    type: Literal["tuplet"] = json_field(["type"])
                    # optional fields:
                    show_number: Optional["DefTupletDisplaySetting"] = json_field(
                        ["showNumber"], default=None
                    )
                    bracket: Optional[
                        Union[Literal["yes"], Literal["no"], Literal["auto"]]
                    ] = json_field(["bracket"], default=None)
                    show_value: Optional["DefTupletDisplaySetting"] = json_field(
                        ["showValue"], default=None
                    )
                    orient: Optional["DefOrientation"] = json_field(
                        ["orient"], default=None
                    )
                    staff: Optional["DefStaffNumber"] = json_field(
                        ["staff"], default=None
                    )

                # required fields:
                content: list[
                    Union[
                        "DefEvent",
                        "ContentChoice1",
                        "ContentChoice2",
                        "ContentChoice3",
                        "ContentChoice4",
                        "ContentChoice5",
                    ]
                ] = json_field(["content"])
                # optional fields:
                voice: Optional["DefVoiceName"] = json_field(["voice"], default=None)
                orient: Optional["DefOrientation"] = json_field(
                    ["orient"], default=None
                )
                staff: Optional["DefStaffNumber"] = json_field(["staff"], default=None)

            @dataclass
            class Clef(JSONWizard):
                @dataclass
                class Clef(JSONWizard):
                    # required fields:
                    staff_position: "DefStaffPosition" = json_field(["staffPosition"])
                    sign: Union[Literal["C"], Literal["F"], Literal["G"]] = json_field(
                        ["sign"]
                    )
                    # optional fields:
                    class_: Optional["DefStyleClass"] = json_field(
                        ["class"], default=None
                    )
                    color: Optional[str] = json_field(["color"], default=None)
                    octave: Optional[int] = json_field(["octave"], default=None)
                    glyph: Optional["DefSmuflGlyph"] = json_field(
                        ["glyph"], default=None
                    )

                @dataclass
                class Position(JSONWizard):
                    # required fields:
                    fraction: list["DefIntegerUnsigned"] = json_field(["fraction"])
                    # optional fields:
                    grace_index: Optional["DefIntegerUnsigned"] = json_field(
                        ["graceIndex"], default=None
                    )

                # required fields:
                clef: "Clef" = json_field(["clef"])
                # optional fields:
                position: Optional["Position"] = json_field(["position"], default=None)

            # required fields:
            sequences: list["Sequence"] = json_field(["sequences"])
            # optional fields:
            clefs: Optional[list["Clef"]] = json_field(["clefs"], default=None)
            beams: Optional["DefBeamList"] = json_field(["beams"], default=None)

        # required fields:
        # optional fields:
        smufl_font: Optional["DefSmuflFont"] = json_field(["smuflFont"], default=None)
        staves: Optional[int] = json_field(["staves"], default=None)
        id: Optional["DefId"] = json_field(["id"], default=None)
        name: Optional[str] = json_field(["name"], default=None)
        short_name: Optional[str] = json_field(["shortName"], default=None)
        measures: Optional[list["Measure"]] = json_field(["measures"], default=None)

    @dataclass
    class Layout(JSONWizard):
        # required fields:
        content: "DefSystemLayoutContent" = json_field(["content"])
        id: "DefId" = json_field(["id"])
        # optional fields:

    @dataclass
    class Score(JSONWizard):
        @dataclass
        class Page(JSONWizard):
            @dataclass
            class System(JSONWizard):
                @dataclass
                class LayoutChange(JSONWizard):
                    # required fields:
                    layout: "DefId" = json_field(["layout"])
                    location: "DefMeasureLocation" = json_field(["location"])
                    # optional fields:

                # required fields:
                measure: "DefMeasureNumber" = json_field(["measure"])
                # optional fields:
                layout_changes: Optional[list["LayoutChange"]] = json_field(
                    ["layoutChanges"], default=None
                )
                layout: Optional["DefId"] = json_field(["layout"], default=None)

            # required fields:
            systems: list["System"] = json_field(["systems"])
            # optional fields:
            layout: Optional["DefId"] = json_field(["layout"], default=None)

        @dataclass
        class MultimeasureRest(JSONWizard):
            # required fields:
            duration: int = json_field(["duration"])
            start: "DefMeasureNumber" = json_field(["start"])
            # optional fields:
            label: Optional[str] = json_field(["label"], default=None)

        # required fields:
        name: str = json_field(["name"])
        # optional fields:
        pages: Optional[list["Page"]] = json_field(["pages"], default=None)
        multimeasure_rests: Optional[list["MultimeasureRest"]] = json_field(
            ["multimeasureRests"], default=None
        )
        layout: Optional["DefId"] = json_field(["layout"], default=None)

    # required fields:
    parts: list["Part"] = json_field(["parts"])
    mnx: "Mnx" = json_field(["mnx"])
    global_: "Global" = json_field(["global"])
    # optional fields:
    scores: Optional[list["Score"]] = json_field(["scores"], default=None)
    layouts: Optional[list["Layout"]] = json_field(["layouts"], default=None)
