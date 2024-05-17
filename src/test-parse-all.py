import mnx
import json
import os
import sys

example_path = "../examples"
output_path = "../outputs"
os.makedirs(output_path, exist_ok=True)
filenames = os.listdir(example_path)
for filename in filenames:
    infilepath = os.path.join(example_path, filename)
    try:
        with open(infilepath, "r") as f:
            inp = f.read()
        out = mnx.Top.from_json(inp)
        outfilepath = os.path.join(output_path, filename)
        with open(outfilepath, "w") as f:
            f.write(out.to_json(indent=2))
    except BaseException as ex:
        print(f"Error parsing file {infilepath}", file=sys.stderr)
        print(ex, file=sys.stderr)
        print("", file=sys.stderr)
