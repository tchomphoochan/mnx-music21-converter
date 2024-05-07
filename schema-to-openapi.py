import json
import sys

forbidden = ['$id', '$schema', '$defs', 'const']

with open('mnx-schema.json', 'r') as file:
  schema = json.load(file)

openapi: dict = {
  "openapi": "3.0.0",
  "info": {
    "title": "MNX",
    "version": "0.0"
  },
  "components": {
    "schemas": {}
  },
  "paths": {}
}

def add_cleaned_schema(name, defn):
  openapi['components']['schemas'][name] = defn

def clean(defn):
  if type(defn) == dict:
    if '$ref' in defn:
      assert len(defn) == 1
      ref = defn['$ref']
      ref = '#/components/schemas/' + ref.split('/')[2]
      return {'$ref': ref}
    else:
      cleaned = {}
      for k, v in defn.items():
        if k in forbidden:
          continue
        cleaned[k] = clean(v)
      return cleaned
  elif type(defn) == list:
    return [clean(v) for v in defn]
  else:
    return defn

for name, defn in schema['$defs'].items():
  add_cleaned_schema(name, clean(defn))
add_cleaned_schema('MNXDocument', clean(schema))

with open('openapi.json', 'w') as file:
  json.dump(openapi, file, indent=2)