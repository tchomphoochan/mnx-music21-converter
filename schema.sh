#!/usr/bin/env zsh

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
java -jar $SCRIPT_DIR/openapi-json-schema-generator/target/openapi-json-schema-generator-cli.jar $@