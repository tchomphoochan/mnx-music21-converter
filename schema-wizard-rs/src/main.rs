pub mod schema;

#[derive(Debug, PartialEq)]
struct Object {
    properties: Vec<Field>
}
impl Eq for Object {}

#[derive(Debug, PartialEq)]
struct Field {
    key: String,
    value_type: Type,
    required: bool
}
impl Eq for Field {}

#[derive(Debug, PartialEq)]
enum Type {
    Integer,
    String,
    StringEnum(Vec<String>),
    Array(Box<Type>),
    Object(Object),
    AnyOf(Vec<Type>),
    Ref(String)
}
impl Eq for Type {}

struct Dataclass {
    name: String,
    subclasses: Vec<Dataclass>,
    fields: Vec<Field>
}

fn main() {
    println!("Hello, world!");
}

fn parse(schema: String) -> Type {
    unimplemented!()
}

mod test {
    use super::*;

    #[test]
    fn integer_type() {
        let input = r#"
        {
            "type": "integer"
        }
        "#.to_string();
        assert_eq!(
            parse(input),
            Type::Integer
        )

    }

    #[test]
    fn object_with_integer() {
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
        "#.to_string();
        assert_eq!(
            parse(input),
            Type::Object(Object {
                properties: vec![
                    Field {
                        key: "hello".to_string(),
                        value_type: Type::Integer,
                        required: true
                    }
                ]
            })
        )

    }

    #[test]
    fn string() {
        let input = r#"
        {
            "type": "string"
        }
        "#.to_string();
        assert_eq!(
            parse(input),
            Type::String
        )
    }

    #[test]
    fn string_enum() {
        let input = r#"
        {
            "type": "string",
            "enum": [
                "hi",
                "hello",
                "bye"
            ]
        }
        "#.to_string();
        assert_eq!(
            parse(input),
            Type::StringEnum(vec![
                "hi".into(),
                "hello".into(),
                "bye".into()
            ])
        )
    }

    #[test]
    fn string_const() {
        let input = r#"
        {
            "type": "string",
            "const": "hello"
        }
        "#.to_string();
        assert_eq!(
            parse(input),
            Type::StringEnum(vec![
                "hello".into()
            ])
        )
    }

    #[test]
    fn array() {
        let input = r#"
        {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
        "#.to_string();
        assert_eq!(
            parse(input),
            Type::Array(Box::new(Type::String))
        )
    }

}