To generate Python data classes,
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