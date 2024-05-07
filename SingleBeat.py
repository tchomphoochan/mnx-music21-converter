from music21 import converter, note, stream, meter

class SingleBeat(converter.subConverters.SubConverter):
    registerFormats = ('singlebeat',)  # note the comma after the string
    registerInputExtensions = ('sb',)  # these are single element tuples.

    # we will just define parseData for now and let the SubConverter base class
    # deal with loading data from files of type .sb and URLs ending in .sb for us.

    def parseData(self, strData, number=None):  # movement number is ignored...
        '''  'AB C' -> A-8th, B-8th, C-qtr '''
        strDataList = strData.split()
        s = stream.Part()
        m = meter.TimeSignature('4/4')
        s.insert(0, m)
        for beat in strDataList:
            ql = 1.0/len(beat)
            for n in beat:
                nObj = note.Note(n)
                nObj.duration.quarterLength = ql
                s.append(nObj)
        self.stream = s.makeMeasures()

converter.registerSubConverter(SingleBeat)

s = converter.parse('CDC DE F GAGB GE C DEFED C', format='singleBeat')
s.show('text')