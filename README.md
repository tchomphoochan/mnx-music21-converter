# MNX to music21 converter

## Results

This document recounts the effort spent on the JSON-schema-to-dataclass converter,
except this section which discusses the MNX converter itself.

A lot of the code for this generator can be quite tricky to run because
it involves some manual error-fixing. I highly recommend doing `git reset --hard`
once you are done playing with it to reset the project to a good state.

The actual project itself is in `src/` and does not need much explanation (I think).

You can run the converter (`convert.py`) through `test-convert-all.ipynb`
to see the results. Alternatively, you can write your own code that has
```py
import mnx
import converter
```
See example at the very bottom of `convert.py`.

I have not had the chance to implement all features described by the MNX spec,
due to other end-of-term obligations and the deadline. Some features are themselves
not implementable because they are poorly specified in the schema.

The Jupyter notebook lists all examples that have been implemented correctly.

Despite the project being incomplete, I hope that it does demonstrate
the feasibility of writing a converter from MNX to music21 and
how one might go about coding it.

Thanks for a great class this semester!

—Pleng

---

## Generating code from JSON schema

While MNX gives us [a specification][mnx-schema] in the form of a [JSON Schema][json-schema],
this is really only useful for validating untyped dictionaries as the beginning.
It does not give us any further expressive power like a strongly typed system would.
If we could generate a code that defines all dataclasses and enums based on the JSON schema,
then writing code based on MNX document objects would be much more convenient.
This is especially important because MNX is still in alpha, meaning we need a way for us
to easily detect when the specification changes (e.g. the field name may have changed).
A type system could help.

---

### Attempt 1: OpenAPI generator

I have looked into how we would accomplish this and found that the closest tool to what we want,
that has most of the required functionalities, is the [OpenAPI JSON Schema Generator](https://github.com/openapi-json-schema-tools/openapi-json-schema-generator).
In its README, you can see cool examples on how generated code creates type hints for objects based on JSON Schemas.

In order to use this, we need to put [the specification][mnx-schema] into a minimal OpenAPI document object.
I have written a simple Python program `schema-to-openapi.py` that helps with this. Note that the MNX schema cannot be used as is,
because it would end up generating a field named `global` which is a reserved Python keyword. Therefore, we will change it to `globals` instead.
When we read in an MNX document, we simply need to make sure to do the same translation so we can use our generated code.

I only had partial success with this and gave up on using it. **The code has not been maintained since, so instructions in this section may be out of date.**

[mnx-schema]: https://w3c.github.io/mnx/docs/mnx-schema.json
[json-schema]: https://json-schema.org/

#### Steps for generating dataclasses

1. Download `mnx-schema.json`
2. Make sure to change all occurences of `global` into `globals` to avoid conflicts with the Python keyword
3. Run the following commands
```sh
python3 schema-to-openapi.py
mkdir target
cd target
mv ../openapi.json .
../schema.sh generate -i openapi.json -g python --package-name "mnx"
```
4. Go into `/target/src` and run `python3 -i` then `from mnx.components.schemas import *`. You will see errors. These are due to recursive schemas. Fix those errors by putting the type names in quotes. For example, `BeamListTupleInput` should become `"BeamListTupleInput"`. Repeat this a few times until all errors disappear.

#### Testing the dataclasses

Continuing from earlier, we can try running the following code (while in `/target/src`)
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
I have spent a lot of time looking into this, but the resulting error messages have not been
very helpful in debugging. I reckon it has something to do with how this code generator tool
does not quite fully support all features of JSON Schema yet. (For example, I have to explicitly
remove the keywords `const` in my conversion script. This means we don't really have
a good way of representing tagged unions with our dataclasses.)

As a result of these issues, I have decided to drop this line of inquiry
and proceeded with working on this project without the type system's help.
Indeed, as you may have noticed, I have not really tried to extract the generated schemas
from `target/src` yet. (It is somewhat tricky, since it also relies on other pieces of generated code,
in a pretty complicated, generated project.) Obviously, this could not be used to contribute to music21.

If one is ever interested in attempting this, I believe it might be the best to
simply write your own JSON-schema-to-Python-dataclasses generator that supports
the subset of features used by the MNX schema. This should generate pretty clean and readable code
and should be fairly minimal.

---

### Attempt 2: Schema wizard in Python

I tried to write my own program to convert JSON schemas into Python dataclasses, using Python.

Those dataclasses leverage another library named `dataclass_wizard`, which uses runtime reflection
to implement automated JSON serializing/deserializing.

Sadly, I was not able to get the generated code to work well. There are too many errors to fix manually.

Fixing the converter code was also quite painful, because Python does not give us a good way to model
the ontologies of the JSON schema and the result we want.

You can see the half-working converter in `schema-wizard-py/schema-converter.py`,
and the result, manually half-cleaned, in `schema-wizard-py/out-manual-clean.py`.

**The code has not been maintained since.**

---

### Attempt 3: Schema wizard in Rust

I decided to try again but using Rust.

I used `serde` and `serde_json` to read in a JSON schema as a strongly typed struct.
It heavily leverages Rust's ability to beautifully express sum types with powerful enums.

Then, I write routines to convert from those structs to dataclass structs, which I modeled
based on how I wanted my Python code to look like.

Things worked pretty well this time. You could generate code by doing the following, assuming you have Rust, Cargo, and Python Black formatter installed. (I have already done this and all the required fixes.)
```sh
cd schema-wizard-rs
cargo run -- -i assets/mnx-schema.json -o ../src/mnx/__init__.py
cd ../src
black .
```

You will notice there are three errors, all of them pertaining to types that are recursively defined.

One might think that those errors are fixable by simply adding
quotation marks around the recursive uses, but the dataclass wizard
will actually fail to generate a working parser. Trying to parse any MNX file will result in stack overflow.

Each run of the generator is non-deterministic because of the use of hash maps. The definitions may show up in different orders, so from now on, the line numbers for `src/mnx/__init__.py` I reference are going to be based on the version that is committed.

On line 275, `DefBeamList` references `DefBeam` which itself references `DefBeamList`.
I changed the definition to just `DefBeamList: TypeAlias = list`.
(Needed to do this because it turns out `TypeAlias` interacts weirdly with the dataclass wizard.
Luckily this is the only problematic place.)

The other error on line 292 is much trickier. Beams are important to this project, so we can't simply ignore them.
I decided to replace the recursive reference with an untyped `dict` and make sure that wherever I reference `DefBeamList.inner`,
I don't forget to manually run the parser for the inner dictionary.

Similarly, on line 48 of `src/mnx/__init__.py`, for `DefSystemLayoutContentChoice0`, I replaced the reference
with `DefSystemLayoutContent` to just an untyped `list`.

One more runtime error: `dataclass_wizard` is actually pretty bad at dealing with parsing unions.
It looks for a very specific pattern indicating the use of discriminated unions.
Luckily, MNX is pretty consistent in this regard, so I decided to add a hack in my `schema-wizard-rs`.
This hack simply adds `JSONWizard.Meta` information to tell JSON wizard how to discriminate the union types.
I also had to manually add these three lines of code inside `class Top` as well (see line 644):
```py
class _(JSONWizard.Meta):
  tag_key = "type"
  auto_assign_tags = True
```

(I could have done this in the code generator, but that's too much effort.)

Finally, I didn't quite implement enums properly and choose to just use `Literal[a, b, c, ...]` to indicate the possibilities.

Now that everything is ready, we can try parsing and re-printing everything.
```sh
cd src
python3 test-parse-all.py
```

When I ran this, there were a few errors. It turned out all of them result from wrong/outdated transcriptions.
I believe those are Kyle's transcriptions rather than official ones. I manually fixed them.
```
Error parsing file ../examples/liszt.json
Failure parsing field `step` in class `DefEvent.Note.Pitch`. Expected a type Literal, got str.
  value: 'Db'
  error: Value not in expected Literal values
  allowed_values: ['A', 'B', 'C', 'D', 'E', 'F', 'G']
  json_object: '{"octave": 2, "step": "Db"}'

Error parsing file ../examples/bach_minuet.json
Failure parsing field `step` in class `DefEvent.Note.Pitch`. Expected a type Literal, got str.
  value: 'F#'
  error: Value not in expected Literal values
  allowed_values: ['A', 'B', 'C', 'D', 'E', 'F', 'G']
  json_object: '{"octave": 5, "step": "F#"}'

Error parsing file ../examples/bach_minuet_rh.json
Failure parsing field `step` in class `DefEvent.Note.Pitch`. Expected a type Literal, got str.
  value: 'F#'
  error: Value not in expected Literal values
  allowed_values: ['A', 'B', 'C', 'D', 'E', 'F', 'G']
  json_object: '{"octave": 5, "step": "F#"}'
```