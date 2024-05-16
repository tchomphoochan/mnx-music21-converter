use std::collections::HashMap;

use serde::{Serialize, Deserialize};

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct TopLevel {
    pub title: String,

    #[serde(default, rename = "$defs")]
    pub defs: HashMap<String, Schema>,

    #[serde(rename = "$id")]
    pub id: String,

    #[serde(rename = "$schema")]
    pub metaschema: String,

    #[serde(rename = "description")]
    pub description: String,

    #[serde(flatten)]
    pub content: Schema
}
impl Eq for TopLevel {}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum Type {
    Schema(Schema),
    AnyOf(AnyOf),
    Ref(Ref)
}
impl Eq for Type {}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct AnyOf {
    #[serde(rename = "anyOf")]
    pub any_of: Vec<Type>
}
impl Eq for AnyOf {}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct Ref {
    #[serde(rename = "$ref")]
    pub ref_id: String
}
impl Eq for Ref {}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "camelCase")]
pub enum Schema {
    Array(ArraySchema),
    Integer(IntegerSchema),
    String(StringSchema),
    Boolean(BooleanSchema),
    Object(ObjectSchema),
}
impl Eq for Schema {}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub struct ArraySchema {
    pub items: Box<Type>
}
impl Eq for ArraySchema {}

#[derive(Default, Debug, PartialEq, Serialize, Deserialize)]
pub struct SingleValueSchema<T> {
    #[serde(default, rename = "const")]
    pub const_value: Option<T>,

    #[serde(default, rename = "enum")]
    pub enum_values: Option<Vec<T>>
}
impl<T> SingleValueSchema<T> where T : Clone {
    pub fn choices(&self) -> Option<Vec<T>> {
        if let Some(v) = self.const_value.as_ref() {
            Some(vec![v.clone()])
        } else {
            self.enum_values.as_ref().map(|x| x.to_owned())
        }
    }
}

pub type IntegerSchema = SingleValueSchema<i32>;
pub type StringSchema = SingleValueSchema<String>;
pub type BooleanSchema = SingleValueSchema<bool>;

#[derive(Default, Debug, PartialEq, Serialize, Deserialize)]
pub struct ObjectSchema {
    pub properties: HashMap<String, Type>,
    
    #[serde(rename = "additionalProperties")]
    pub additional_properties: bool,

    #[serde(default)]
    pub required: Vec<String>
}
impl Eq for ObjectSchema {}

#[cfg(test)]
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