import mnx
import json
import os
import sys

top: mnx.Top = mnx.Top(
    mnx=mnx.Top.Mnx(version=1),
    global_=mnx.Top.Global(
        measures=[
            mnx.Top.Global.Measure(
                barline=mnx.Top.Global.Measure.Barline(type="regular"),
                time=mnx.Top.Global.Measure.Time(count=4, unit=4),
            )
        ]
    ),
    parts=[
        mnx.Top.Part(
            measures=[
                mnx.Top.Part.Measure(
                    clefs=[
                        mnx.Top.Part.Measure.Clef(
                            clef=mnx.Top.Part.Measure.Clef.Clef(
                                sign="G", staff_position=-2
                            )
                        )
                    ],
                    sequences=[
                        mnx.Top.Part.Measure.Sequence(
                            content=[
                                mnx.DefEvent(
                                    type="event",
                                    duration=mnx.DefNoteValue(base="whole"),
                                    notes=[
                                        mnx.DefEvent.Note(
                                            pitch=mnx.DefEvent.Note.Pitch(
                                                octave=4, step="C"
                                            )
                                        )
                                    ],
                                )
                            ]
                        )
                    ],
                )
            ]
        )
    ],
)

print(top.to_json(indent=2))