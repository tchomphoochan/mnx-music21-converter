# MNX to music21 converter

## Generating code from JSON schema

While MNX gives us [a specification][mnx-schema] in the form of a [JSON Schema][json-schema],
this is really only useful for validating untyped dictionaries as the beginning.
It does not give us any further expressive power like a strongly typed system would.
If we could generate a code that defines all dataclasses and enums based on the JSON schema,
then writing code based on MNX document objects would be much more convenient.
This is especially important because MNX is still in alpha, meaning we need a way for us
to easily detect when the specification changes (e.g. the field name may have changed).
A type system could help.

I have looked into how we would accomplish this and found that the closest tool to what we want,
that has most of the required functionalities, is the [OpenAPI JSON Schema Generator](https://github.com/openapi-json-schema-tools/openapi-json-schema-generator).
In its README, you can see cool examples on how generated code creates type hints for objects based on JSON Schemas.

In order to use this, we need to put [the specification][mnx-schema] into a minimal OpenAPI document object.
I have written a simple Python program `schema-to-openapi.py` that helps with this. Note that the MNX schema cannot be used as is,
because it would end up generating a field named `global` which is a reserved Python keyword. Therefore, we will change it to `globals` instead.
When we read in an MNX document, we simply need to make sure to do the same translation so we can use our generated code.

I only had partial success with this, so this is not really used in the project. (The project is meant to be a prototype anyway.)

[mnx-schema]: https://w3c.github.io/mnx/docs/mnx-schema.json
[json-schema]: https://json-schema.org/

### Steps for generating dataclasses

1. Download `mnx-schema.json`
2. Make sure to change all occurences of `global` into `globals` to avoid conflicts with the Python keyword
3. Run the following commands
```
python3 schema-to-openapi.py
mkdir target
cd target
mv ../openapi.json .
../schema.sh generate -i openapi.json -g python --package-name "mnx"
```
4. Go into `/target/src` and run `python3 -i` then `from mnx.components.schemas import *`. You will see errors. These are due to recursive schemas. Fix those errors by putting the type names in quotes. For example, `BeamListTupleInput` should become `"BeamListTupleInput"`. Repeat this a few times until all errors disappear.

### Testing the dataclasses

Continuing from earlier, we can try running the following code
```py
import json
import os
from mnx.components.schemas import *

def read_mnx_file(filename: str) -> dict:
  with open(filename, 'r') as f:
    d = json.load(f)
  d['globals'] = d['global']
  del d['global']
  return d

for name in sorted(list(os.listdir('../../examples'))):
  try:
    path = '../../examples/' + name
    result = MNXDocument.validate(read_mnx_file(path))
    print(f'Successfully validated {name}. Measures: {len(result.globals.measures)}')
  except:
    print(f'Failed to validate {name}')
```
The result is
```
Failed to validate bach_minuet.json
Failed to validate bach_minuet_rh.json
Successfully validated example_accidentals.json. Measures: 3
Successfully validated example_articulations.json. Measures: 1
Successfully validated example_beam_hooks.json. Measures: 1
Successfully validated example_beams.json. Measures: 2
Successfully validated example_beams_across_barlines.json. Measures: 2
Successfully validated example_dotted_notes.json. Measures: 1
Successfully validated example_grace.json. Measures: 1
Successfully validated example_grace_beams.json. Measures: 1
Successfully validated example_grace_in_beam.json. Measures: 1
Successfully validated example_hello_world.json. Measures: 1
Successfully validated example_key_signatures.json. Measures: 4
Successfully validated example_multiple_voices.json. Measures: 2
Successfully validated example_parts.json. Measures: 2
Successfully validated example_repeats.json. Measures: 1
Successfully validated example_repeats_alternate_endings_advanced@.json. Measures: 6
Successfully validated example_rest_positions.json. Measures: 1
Successfully validated example_secondary_beam_breaks@.json. Measures: 1
Successfully validated example_slurs.json. Measures: 2
Successfully validated example_slurs_chords.json. Measures: 1
Successfully validated example_slurs_incomplete.json. Measures: 1
Failed to validate example_slurs_targeted@.json
Successfully validated example_three_note_chord_half_rest.json. Measures: 1
Successfully validated example_ties.json. Measures: 2
Successfully validated example_time_signatures.json. Measures: 3
Successfully validated example_tuplets.json. Measures: 2
Successfully validated example_two_bar_c_major_scale.json. Measures: 2
Failed to validate liszt.json
```
As you can see, in the code, we are able to access `result.globals.measures`. Thanks, type system.
However, it seems like we are still having trouble validating some pieces.