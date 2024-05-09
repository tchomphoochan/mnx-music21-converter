import sys
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import *

import pprint

reserved = ['class', 'global', 'type']

@dataclass
class JsonClass():
  name: str
  subclasses: list[Union['JsonClass','JsonAlias']]
  requiredFields: list[Tuple[str, str]]
  optionalFields: list[Tuple[str, str]]

class JsonClassPrinter():
  jsonClass: JsonClass
  result: str
  layer: int
  def __init__(self, jsonClass):
    self.jsonClass = jsonClass
  
  def compute(self):
    self.result = ""
    self.layer = 0

    self.work(self.jsonClass)
  
  def line(self, msg: str):
    self.result += "  " * self.layer
    self.result += msg
    self.result += '\n'

  def work(self, c: Union[JsonClass,'JsonAlias']):
    if isinstance(c, JsonAlias):
      # TypeAlias
      self.line(f"{nice_name(c.key)} = {c.value}")
      return

    self.line('@dataclass')
    print(c, file=sys.stderr)
    self.line(f'class {c.name}(JSONWizard):')
    self.layer += 1
    try:
      for subclass in c.subclasses:
        self.work(subclass)
      self.line("# Required fields")
      for name, type in c.requiredFields:
        if name in reserved:
          k = "_" + name
        else:
          k = name
        self.line(f"{k}: {type} = json_field(['{name}'])")
      if c.requiredFields == []:
        self.line("pass")
      self.line("# Optional fields")
      for name, type in c.optionalFields:
        if name in reserved:
          k = "_" + name
        else:
          k = name
        oldtype = type
        if 'list' in type:
          type = 'list'
        elif type == c.name:
          type = 'lambda *args, **kwargs: None'
        self.line(f"{k}: {oldtype} = json_field(['{name}'], default_factory={type})")
      if c.optionalFields == []:
        self.line("pass")
    finally:
      self.layer -= 1

@dataclass
class JsonAlias:
  key: str
  value: str
  
def capitalize(name: str) -> str:
  return name[0].upper() + name[1:]

def nice_name(name: str) -> str:
  if '/' in name:
    name = name.split('/')[2]
  return "".join([capitalize(x) for x in name.split('-')])

def parse_property(key: str, property: dict) -> Tuple[str, List[Union[JsonClass, JsonAlias]]]:
  match property:
    case {"type": "integer"}:
      n = nice_name(key)
      return n, [JsonAlias(n, "int")]
    case {"type": "string"}:
      n = nice_name(key)
      return n, [JsonAlias(n, "str")]
    case {"const": x}:
      n = nice_name(key)
      return n, [JsonAlias(n, f"Literal[{repr(x)}]")]
    case {"type": "boolean"}:
      n = nice_name(key)
      return n, [JsonAlias(n, f"bool")]
    case {"type": "array", "items": itemSchema}:
      type, cls = parse_property(key.rstrip('s'), itemSchema)
      return f"list[{type}]", cls
    case {
      "type": "object",
      "additionalProperties": additionalProperties,
      "properties": properties,
      **rest
    }:
      assert additionalProperties == False, "We only handle additionalProperties = False"
      requiredFields = rest.get('required', [])
      subclasses = []
      required = []
      optional = []
      for k, p in properties.items():
        type, subclass = parse_property(k, p)
        subclasses.extend(subclass)
        if k in requiredFields:
          required.append((k, type))
        else:
          optional.append((k, type))
      # assert not key.endswith('s'), (key, property)
      n = nice_name(key)
      return n, [JsonClass(n, subclasses, required, optional)]
    case {"$ref": name}:
      n = nice_name(name)
      return "Def" + n, []
    case {"anyOf": choices}:
      names = []
      classes = []
      for i, choice in enumerate(choices):
        n, cs = parse_property(f'{key}-choice-{i:02d}', choice)
        names.append(n)
        classes.extend(cs)
      un = 'Union[' + ", ".join(names) + ']'
      n = nice_name(key)
      return n, (classes + [JsonAlias(n, un)])
    case _:
      raise Exception()

with open('mnx-schema.json', 'r') as f:
  d = json.load(f)

print("from dataclasses import dataclass, field")
print("from datetime import date")
print("from enum import Enum")
print("from typing import *")
print("from dataclass_wizard import JSONWizard, json_field  # mypy: ignore")
print("")

cs = []
for k, v in d['$defs'].items():
  n, _cs = parse_property('def-'+k, v)
  cs.extend(_cs)

for c in cs:
  if isinstance(c, JsonAlias):
    p = JsonClassPrinter(c)
    p.compute()
    print(p.result)
for c in cs:
  if not isinstance(c, JsonAlias):
    p = JsonClassPrinter(c)
    p.compute()
    print(p.result)

n, cs = parse_property("mnx-document", d)

for c in cs:
  if isinstance(c, JsonAlias):
    p = JsonClassPrinter(c)
    p.compute()
    print(p.result)
for c in cs:
  if not isinstance(c, JsonAlias):
    p = JsonClassPrinter(c)
    p.compute()
    print(p.result)