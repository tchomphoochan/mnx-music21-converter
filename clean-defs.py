import sys
import json
import copy

with open('mnx-schema.json', 'r') as file:
  schema = json.load(file)

layer = 0
cleaned_defs: dict[str, dict|None] = {}

def clean(key: str, defn: dict|list) -> dict|list:
  global layer
  layer += 1
  print('  ' * (layer-1), end='')
  print(f'{key}:', defn)

  new_defn: dict|list
  if type(defn) == dict:
    new_defn = {}

    if '$ref' in defn:
      name = defn['$ref']
      content = get(name)
      if content is None:
        new_defn = defn # do nothing
      else:
        new_defn = content
    else:
      for k, v in defn.items():
        new_defn[k] = clean(k, v)
  
  elif type(defn) == list:
    new_defn = [clean(f'.{i}', x) for i, x in enumerate(defn)]
  
  else:
    new_defn = defn

  layer -= 1
  return new_defn

def get(fullname: str) -> dict|None:
  global layer
  layer += 1
  print('  ' * (layer-1), end='')
  name = fullname.split('/')[2]
  if name in cleaned_defs:
    r = cleaned_defs[name]
    if r is None:
      print(f'get({name}): recursion found')
      layer -= 1
      return None
    else:
      print(f'get({name}): already computed')
      layer -= 1
      return cleaned_defs[name]
  print(f'get({name}): computing...')
  cleaned_defs[name] = None
  cleaned = clean(fullname, schema['$defs'][name])
  assert type(cleaned) == dict
  cleaned_defs[name] = cleaned
  layer -= 1
  return cleaned
  
cleaned = clean('schema', schema)
assert type(cleaned) == dict
del cleaned['$defs']
with open('mnx-schema-cleaned.json', 'w') as file:
  json.dump(cleaned, file, sort_keys=True, indent=2)