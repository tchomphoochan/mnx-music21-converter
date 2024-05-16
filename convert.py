from music21 import converter, note, stream, meter
import json


class MNXConverter(converter.subConverters.SubConverter):
    registerFormats = ("mnx",)
    registerInputExtensions = ("json",)

    def parseData(self, strData: str, number: int | None = None) -> None:
        mnxDoc: dict = json.loads(strData)

        # do something
        self.stream = stream.Score()


converter.registerSubConverter(MNXConverter)

s = converter.parse("examples/bach_minuet.json", format="mnx")
s.show(makeNotation=False)
