from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from dataclass_wizard import JSONWizard, json_field  # mypy: ignore

Globals = dict
MNXMetadata= dict
Mnx = dict
Part = dict
Layout = dict
Score = dict

@dataclass
class MNXDocument(JSONWizard):

  @dataclass
  class Globals(JSONWizard):

    @dataclass
    class Measure(JSONWizard):

      @dataclass
      class Barline(JSONWizard):
        class BarlineType(Enum):
          REGULAR = "regular"
          DOTTED = "dotted"
          DASHED = "dashed"
          HEAVY = "heavy"
          LIGHT_LIGHT = "light-light"
          LIGHT_HEAVY = "light-heavy"
          HEAVY_LIGHT = "heavy-light"
          TICK = "tick"
          SHORT = "short"
          NONE = "none"
        type: BarlineType
      
      @dataclass
      class Ending(JSONWizard):
        # required
        duration: int = json_field(['duration'])
        # optional
        styleClass: dict = json_field(['class'], default_factory=dict)
        color: str = json_field(['color'], default="")
        numbers: list[int] = json_field(['number'], default_factory=list)
        open: bool = json_field(['open'], default=False)

      # required
      # none
      # optional
      barline: Barline = json_field(['barline'], default_factory=dict)
      ending: Ending = json_field(['ending'], default_factory=dict)
      fine: dict = json_field(['fine'], default_factory=dict)
      index: dict = json_field(['index'], default_factory=dict)
      jump: dict = json_field(['jump'], default_factory=dict)
      key: dict = json_field(['key'], default_factory=dict)
      number: dict = json_field(['number'], default_factory=dict)
      repeatEnd: dict = json_field(['repeatEnd'], default_factory=dict)
      repeatStart: dict = json_field(['repeatStart'], default_factory=dict)
      segno: dict = json_field(['segno'], default_factory=dict)
      tempos: dict = json_field(['tempo'], default_factory=dict)
      time: dict = json_field(['time'], default_factory=dict)

    Style = dict

    # required
    measures: list[Measure] = json_field(['measures'])
    # optional
    styles: list[Style] = json_field(['styles'], default_factory=list)
  
  # required
  globals: Globals = json_field(['global'])
  mnx: MNXMetadata = json_field(['mnx'])
  parts: list[Part] = json_field(['parts'])
  # optional
  layouts: list[Layout] = json_field(['layouts'], default_factory=list)
  scores: list[Score] = json_field(['scores'], default_factory=list)

import json
with open('examples/bach_minuet.json', 'r') as f:
  d = json.load(f)

doc = MNXDocument.from_dict(d)