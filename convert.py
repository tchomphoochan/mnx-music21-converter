from music21 import converter, note, stream, meter
import json

class MNXConverter(converter.subConverters.SubConverter):
  registerFormats = ('mnx',)
  registerInputExtensions = ('mnx',)

  def parseData(self, strData: str, number: int|None=None) -> None:
    mnxDoc: dict = json.loads(strData)

converter.registerSubConverter(MNXConverter)

s = converter.parse('CDC DE F GAGB GE C DEFED C', format='singleBeat')
s.show('text')