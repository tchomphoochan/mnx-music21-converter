use serde_json::json;

pub mod schema;
pub mod dataclass;

fn main() {
    let input = std::fs::read_to_string("assets/mnx-schema.json").unwrap();
    let top: schema::Type = serde_json::from_str(&input).unwrap();
    let (defs, typ) = dataclass::parse("top", &top);
    let s = dataclass::DataclassPrinter::print(defs.get(0).unwrap());
    println!("{}", s)
}

// mod test {
//     use serde::Serialize;
//     use serde_json::json;

//     use crate::schema;

//     use super::*;

//     #[test]
//     fn integer_type() {
//         let input = r#"
//         {
//             "type": "integer"
//         }
//         "#.to_string();
//         assert_eq!(
//             parse(input),
//             Type::Integer
//         )

//     }

//     #[test]
//     fn object_with_integer() {
//         let input = r#"
//         {
//             "additionalProperties": false,
//             "properties": {
//                 "hello": {
//                     "type": "integer"
//                 }
//             },
//             "type": "object",
//             "required": [
//                 "hello"
//             ]
//         }
//         "#.to_string();
//         assert_eq!(
//             parse(input),
//             Type::Object(Object {
//                 properties: vec![
//                     Field {
//                         key: "hello".to_string(),
//                         value_type: Type::Integer,
//                         required: true
//                     }
//                 ]
//             })
//         )

//     }

//     #[test]
//     fn string() {
//         let input = r#"
//         {
//             "type": "string"
//         }
//         "#.to_string();
//         assert_eq!(
//             parse(input),
//             Type::String
//         )
//     }

//     #[test]
//     fn string_enum() {
//         let input = r#"
//         {
//             "type": "string",
//             "enum": [
//                 "hi",
//                 "hello",
//                 "bye"
//             ]
//         }
//         "#.to_string();
//         assert_eq!(
//             parse(input),
//             Type::StringEnum(vec![
//                 "hi".into(),
//                 "hello".into(),
//                 "bye".into()
//             ])
//         )
//     }

//     #[test]
//     fn string_const() {
//         let input = r#"
//         {
//             "type": "string",
//             "const": "hello"
//         }
//         "#.to_string();
//         assert_eq!(
//             parse(input),
//             Type::StringEnum(vec![
//                 "hello".into()
//             ])
//         )
//     }

//     #[test]
//     fn array() {
//         let input = r#"
//         {
//             "type": "array",
//             "items": {
//                 "type": "string"
//             }
//         }
//         "#.to_string();
//         assert_eq!(
//             parse(input),
//             Type::Array(Box::new(Type::String))
//         )
//     }

//     #[test]
//     fn complex_array_object() {
//         let inner_item = json!(
//             {
//                 "type": "object",
//                 "additionalProperties": false,
//                 "properties": {
//                     "word": {
//                         "type": "string"
//                     },
//                     "num": {
//                         "type": "integer"
//                     }
//                 },
//                 "required": [
//                     "word"
//                 ]
//             }
//         );
//         let input_item = json!(
//             {
//                 "type": "object",
//                 "additionalProperties": false,
//                 "properties": {
//                     "things": {
//                         "type": "array",
//                         "items": inner_item
//                     },
//                     "tag": {
//                         "type": "string",
//                         "enum": [
//                             "A",
//                             "B"
//                         ]
//                     }
//                 },
//                 "required": [
//                     "tag"
//                 ]
//             }
//         );
//         let input: schema::Type = serde_json::from_value(input_item).unwrap();
//         let output = parse(serde_json::to_string(&input).unwrap().into());
//         assert_eq!(
//             output,
//             Type::Object(Object {
//                 properties: vec![
//                     Field::new("things".into(), Type::Array(Box::new(Type::Object(Object {
//                         properties: vec![
//                             Field::new("word".into(), Type::String, true),
//                             Field::new("num".into(), Type::Integer, false),
//                         ]
//                     }))), false),
//                     Field::new("tag".into(), Type::StringEnum(vec![
//                         "A".into(),
//                         "B".into(),
//                     ]), true),
//                 ]
//             })
//         )
//     }

// }