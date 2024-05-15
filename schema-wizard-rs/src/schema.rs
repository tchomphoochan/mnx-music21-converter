use std::collections::HashMap;

use serde::{Serialize, Deserialize};

#[derive(Debug, PartialEq, Serialize, Deserialize)]
struct TopLevel {
    title: String,

    #[serde(default, rename = "$defs")]
    defs: HashMap<String, Schema>,

    #[serde(rename = "$id")]
    id: String,

    #[serde(rename = "$schema")]
    metaschema: String,

    #[serde(rename = "description")]
    description: String,

    #[serde(flatten)]
    content: Schema
}
impl Eq for TopLevel {}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
enum Type {
    Schema(Schema),
    AnyOf(AnyOf),
    Ref(Ref)
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
struct AnyOf {
    #[serde(rename = "anyOf")]
    any_of: Vec<Type>
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
struct Ref {
    #[serde(rename = "$ref")]
    ref_id: String
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "camelCase")]
enum Schema {
    Array(ArraySchema),
    Integer(IntegerSchema),
    String(StringSchema),
    Boolean(BooleanSchema),
    Object(ObjectSchema),
}
impl Eq for Schema {}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
struct ArraySchema {
    items: Box<Type>
}
impl Eq for ArraySchema {}

#[derive(Default, Debug, PartialEq, Serialize, Deserialize)]
struct IntegerSchema {

    #[serde(default, rename = "const")]
    const_value: Option<i32>,

    #[serde(default, rename = "enum")]
    enum_values: Option<Vec<i32>>
}
impl Eq for IntegerSchema {}

#[derive(Default, Debug, PartialEq, Serialize, Deserialize)]
struct StringSchema {

    #[serde(default, rename = "const")]
    const_value: Option<String>,

    #[serde(default, rename = "enum")]
    enum_values: Option<Vec<String>>
}
impl Eq for StringSchema {}

#[derive(Default, Debug, PartialEq, Serialize, Deserialize)]
struct BooleanSchema {

    #[serde(default, rename = "const")]
    const_value: Option<bool>,

    #[serde(default, rename = "enum")]
    enum_values: Option<Vec<bool>>
}
impl Eq for BooleanSchema {}

#[derive(Default, Debug, PartialEq, Serialize, Deserialize)]
struct ObjectSchema {
    properties: HashMap<String, Type>,
    
    #[serde(rename = "additionalProperties")]
    additional_properties: bool,

    #[serde(default)]
    required: Vec<String>
}
impl Eq for ObjectSchema {}

mod test {
    use super::*;

    #[test]
    fn bool_schema() -> () {
        let input = r#"{
            "type": "boolean"
        }"#;
        let schema: Schema = serde_json::from_str(input).unwrap();

        assert_eq!(
            schema,
            Schema::Boolean(BooleanSchema {
                const_value: None,
                enum_values: None
            })
        )
    }

    #[test]
    fn integer_schema() -> () {
        let input = r#"{
            "type": "integer"
        }"#;
        let schema: Schema = serde_json::from_str(input).unwrap();

        assert_eq!(
            schema,
            Schema::Integer(IntegerSchema {
                const_value: None,
                enum_values: None
            })
        )
    }

    #[test]
    fn integer_schema_with_const() -> () {
        let input = r#"{
            "type": "integer",
            "const": 5
        }"#;
        let schema: Schema = serde_json::from_str(input).unwrap();

        assert_eq!(
            schema,
            Schema::Integer(IntegerSchema {
                const_value: Some(5),
                enum_values: None
            })
        )
    }

    #[test]
    fn integer_schema_with_enum() -> () {
        let input = r#"{
            "type": "integer",
            "enum": [
                5, 10, 15
            ]
        }"#;
        let schema: Schema = serde_json::from_str(input).unwrap();

        assert_eq!(
            schema,
            Schema::Integer(IntegerSchema {
                const_value: None,
                enum_values: Some(vec![5, 10, 15])
            })
        )
    }

    #[test]
    fn simple_object_schema() -> () {
        let input = r#"
        {
            "additionalProperties": false,
            "properties": {
                "hello": {
                    "type": "integer"
                }
            },
            "type": "object",
            "required": [
                "hello"
            ]
        }
        "#;

        let schema: Schema = serde_json::from_str(input).unwrap();

        assert_eq!(
            schema,
            Schema::Object(ObjectSchema {
                properties: HashMap::from([
                    ("hello".into(), Type::Schema(Schema::Integer(IntegerSchema::default())))
                ]),
                additional_properties: false,
                required: vec!["hello".into()]
            })
        )

    }

    #[test]
    fn simple_array_schema() -> () {
        let input = r#"
        {
            "type": "array",
            "items": {
                "type": "integer"
            }
        }
        "#;

        let schema: Schema = serde_json::from_str(input).unwrap();

        assert_eq!(
            schema,
            Schema::Array(ArraySchema {
                items: Box::new(Type::Schema(Schema::Integer(IntegerSchema::default())))
            })
        )
    }

    #[test]
    fn ref_schema() -> () {
        let input = r#"
        {
            "$ref": "idk"
        }
        "#;

        let schema: Type = serde_json::from_str(input).unwrap();

        assert_eq!(
            schema,
            Type::Ref(Ref { ref_id: "idk".into() })
        )
    }


    #[test]
    fn anyof_schema() -> () {
        let input = r#"
        {
            "anyOf": [
                {
                    "type": "integer"
                },
                {
                    "type": "string"
                }
            ]
        }
        "#;

        let schema: Type = serde_json::from_str(input).unwrap();

        assert_eq!(
            schema,
            Type::AnyOf(AnyOf {
                any_of: vec![
                    Type::Schema(Schema::Integer(IntegerSchema::default())),
                    Type::Schema(Schema::String(StringSchema::default())),
                ]
            })
        )
    }

    #[test]
    fn top_level_schema() -> () {
        let input = r#"
        {
            "$id": "http://localhost:8080/schema.json",
            "$defs": {},
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "test",
            "description": "A test encoding",
            "additionalProperties": false,
            "properties": {
                "hello": {
                    "type": "integer"
                }
            },
            "type": "object",
            "required": [
                "hello"
            ]
        }
        "#;

        let schema: TopLevel = serde_json::from_str(input).unwrap();

        assert_eq!(
            schema,
            TopLevel {
                id: "http://localhost:8080/schema.json".into(),
                defs: HashMap::new(),
                metaschema: "https://json-schema.org/draft/2020-12/schema".into(),
                title: "test".into(),
                description: "A test encoding".into(),
                content: Schema::Object(ObjectSchema {
                    properties: HashMap::from([
                        ("hello".into(), Type::Schema(Schema::Integer(IntegerSchema::default())))
                    ]),
                    additional_properties: false,
                    required: vec!["hello".into()]
                })
            }
        )
    }

    #[test]
    fn try_mnx() -> () {
        let input = std::fs::read_to_string("assets/mnx-schema.json").unwrap();
        let _: TopLevel = serde_json::from_str(&input).unwrap();
    }
}