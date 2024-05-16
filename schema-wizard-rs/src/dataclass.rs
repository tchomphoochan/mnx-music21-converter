use std::collections::{HashMap, HashSet};
use std::fmt;

use convert_case::{Case, Casing};

use crate::schema::{self, Schema};

#[derive(Debug, PartialEq, Eq)]
enum Def {
    Alias(Type),
    Dataclass(Dataclass)
}

#[derive(Debug, PartialEq)]
pub struct Defs {
    definitions: HashMap<String, Def>,
    dependencies: HashMap<String, HashSet<String>>, // deps[x] = {y | y must execute before x}
}
impl Eq for Defs {}
impl Defs {
    fn new() -> Self {
        Defs {
            definitions: HashMap::new(),
            dependencies: HashMap::new()
        }
    }
    fn add_definition(&mut self, name: &str, def: Def) {
        let name = make_class_name(name);
        let refs = match &def {
            Def::Alias(typ) => typ.get_refs(),
            Def::Dataclass(dc) => dc.get_refs()
        };
        self.definitions.insert(name.clone(), def);
        self.dependencies.insert(name.clone(), refs);
    }
}

#[derive(Debug, PartialEq, Eq, Clone)]
enum SortStatus {
    Unvisited,
    Pending,
    Done
}
struct DefsSorter<'a> {
    defs: &'a Defs,
    statuses: HashMap<String, SortStatus>,
    output: Vec<String>,
    has_cycle: bool
}
impl<'a> DefsSorter<'a> {
    fn compute_order(defs: &'a Defs) -> Vec<String> {
        let mut sorter = DefsSorter { defs: defs, statuses: HashMap::new(), output: Vec::new(), has_cycle: false };

        // initialize
        for name in defs.definitions.keys() {
            sorter.statuses.insert(name.to_string(), SortStatus::Unvisited);
        }

        // visit each unvisited node to populate output
        for name in defs.dependencies.keys() {
            match *sorter.statuses.get(name).unwrap() {
                SortStatus::Unvisited => sorter.visit(name),
                SortStatus::Pending => panic!("should not be pending!"),
                SortStatus::Done => (),
            }
        }
        
        // return the output
        sorter.output
    }
    fn visit(&mut self, name: &str) {
        match self.statuses.get(name).unwrap() {
            SortStatus::Unvisited => {
                *self.statuses.get_mut(name).unwrap() = SortStatus::Pending;
                let prereqs = self.defs.dependencies.get(name).unwrap().clone();
                for prereq in prereqs.iter() {
                    self.visit(prereq)
                }
                *self.statuses.get_mut(name).unwrap() = SortStatus::Done;
                self.output.push(name.into())
            },
            SortStatus::Pending => { self.has_cycle = true },
            SortStatus::Done => ()
        }
    }
}

#[derive(Debug, PartialEq)]
pub struct Enum<T> {
    name: String,
    items: Vec<T>
}
impl<T> Eq for Enum<T> where T : Eq {}

#[derive(Debug, PartialEq)]
pub struct Dataclass {
    name: String,
    subclasses: HashMap<String, Dataclass>,
    fields: HashMap<String, Field>
}
impl Eq for Dataclass {}

impl Dataclass {
    fn get_refs(&self) -> HashSet<String> {
        let mut refs = HashSet::<String>::new();
        self.populate_refs(&mut refs);
        refs
    }
    fn populate_refs(&self, refs: &mut HashSet<String>) {
        for (_, subclass) in self.subclasses.iter() {
            subclass.populate_refs(refs)
        }
        for (_, field) in self.fields.iter() {
            field.value_type.populate_refs(refs)
        }
    }
}

#[derive(Debug, PartialEq)]
pub struct Field {
    key: String,
    json_key: String,
    value_type: Type,
    required: bool
}
impl Eq for Field {}
impl Field {
    fn new(key: &str, value_type: Type, required: bool) -> Self {
        Field { key: to_safe_key(&make_field_name(key)), json_key: key.to_string(), value_type, required }
    }
}
impl fmt::Display for Field {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.required {
            write!(f, "{}: {} = json_field(['{}'])", self.key, self.value_type.get_type_name(), self.json_key)
        } else {
            write!(f, "{}: Optional[{}] = json_field(['{}'], default=None)", self.key, self.value_type.get_type_name(), self.json_key)
        }
    }
}

fn to_safe_key(s: &str) -> String {
    match s {
        "global" => "global_",
        "class" => "class_",
        _ => s
    }.to_string()
}

#[derive(Debug, PartialEq)]
pub enum Type {
    Integer,
    IntegerLiteral(i32),
    String,
    StringLiteral(String),
    Boolean,
    BooleanLiteral(bool),
    TypeName(String),
    List(Box<Type>),
    Union(Vec<Type>)
}
impl Eq for Type {}
impl Type {
    fn get_type_name(&self) -> String {
        match self {
            Type::Integer => "int".into(),
            Type::String => "str".into(),
            Type::Boolean => "bool".into(),
            Type::TypeName(x) => format!("'{}'", x),
            Type::List(inner_type) => format!("list[{}]", inner_type.as_ref().get_type_name()),
            Type::Union(types) => {
                let names: Vec<String> = types.iter().map(|typ| typ.get_type_name()).collect();
                format!("Union[{}]", names.join(", "))
            }
            Type::IntegerLiteral(x) => format!("Literal[{}]", x),
            Type::StringLiteral(x) => format!("Literal['{}']", x),
            Type::BooleanLiteral(x) => match x {
                true => "True".into(),
                false => "False".into()
            }
        }
    }
    fn get_refs(&self) -> HashSet<String> {
        let mut refs = HashSet::new();
        self.populate_refs(&mut refs);
        refs
    }
    fn populate_refs(&self, refs: &mut HashSet<String>) {
        match self {
            Type::Integer => (),
            Type::IntegerLiteral(_) => (),
            Type::String => (),
            Type::StringLiteral(_) => (),
            Type::Boolean => (),
            Type::BooleanLiteral(_) => (),
            Type::TypeName(name) => {
                let is_def = make_class_name(&name).starts_with("Def");
                if is_def {
                    refs.insert(name.into());
                }
            },
            Type::List(t) => t.populate_refs(refs),
            Type::Union(ts) => ts.iter().for_each(|t| t.populate_refs(refs)),
        }
    }
}

fn singularize_name(name: &str) -> String {
    name.trim_end_matches("s").to_string()
}

fn make_field_name(name: &str) -> String {
    name.to_case(Case::Snake)
}

fn make_class_name(name: &str) -> String {
    name.to_case(Case::Pascal)
}

fn resolve_ref(name: &str) -> String {
    let parts: Vec<&str> = name.split("/").collect();
    let mut ret = parts.get(2).unwrap().to_string();
    ret.insert_str(0, "def-");
    ret
}

pub fn parse_top(name: &str, top: &schema::TopLevel) -> (Defs, Dataclass) {
    // initialize the definitions-dependencies manager
    let mut definitions = Defs::new();

    // for each def in the schema
    for (name, scm) in top.defs.iter() {
        // parse the def
        let mut name = name.to_string();
        name.insert_str(0, "def-");
        let (defs, typ) = parse_dataclass(&name, scm);
        definitions.add_definition(&name, Def::Alias(typ));
        // if the def is an object (i.e. a class definition):
        for (name, def) in defs.into_iter() {
            definitions.add_definition(&name, Def::Dataclass(def));
        }
    }

    // now parse the main schema content
    let (defs, _typ) = parse_dataclass(name, &top.content);
    assert!(defs.len() == 1);
    let mut defs: Vec<Dataclass> = defs.into_iter().map(|(_k,v)| v).collect();
    let dc = defs.pop().unwrap();

    (definitions, dc)
}

pub fn parse_dataclass(name: &str, typ: &schema::Type) -> (HashMap<String, Dataclass>, Type) {
    match typ {
        schema::Type::Schema(sch) => match sch {
            Schema::Array(sch) => {
                let (defs, typ) = parse_dataclass(&singularize_name(&name), &*sch.items);
                (defs, Type::List(Box::new(typ)))
            },
            Schema::Integer(sch) => match sch.choices() {
                Some(choices) => {
                    if choices.len() == 0 {
                        panic!("Empty enum for an integer schema.")
                    } else if choices.len() == 1 {
                        (HashMap::new(), Type::IntegerLiteral(choices.get(0).unwrap().clone()))
                    } else {
                        let results: Vec<Type> = choices.iter().map(|x| Type::IntegerLiteral(x.clone())).collect();
                        (HashMap::new(), Type::Union(results))
                    }

                },
                None => (HashMap::new(), Type::Integer),
            },
            Schema::String(sch) => match sch.choices() {
                Some(choices) => {
                    if choices.len() == 0 {
                        panic!("Empty enum for an string schema.")
                    } else if choices.len() == 1 {
                        (HashMap::new(), Type::StringLiteral(choices.get(0).unwrap().clone()))
                    } else {
                        let results: Vec<Type> = choices.iter().map(|x| Type::StringLiteral(x.clone())).collect();
                        (HashMap::new(), Type::Union(results))
                    }

                },
                None => (HashMap::new(), Type::String),
            },
            Schema::Boolean(sch) => match sch.choices() {
                Some(choices) => {
                    if choices.len() == 0 {
                        panic!("Empty enum for an string schema.")
                    } else if choices.len() == 1 {
                        (HashMap::new(), Type::BooleanLiteral(choices.get(0).unwrap().clone()))
                    } else {
                        let results: Vec<Type> = choices.iter().map(|x| Type::BooleanLiteral(x.clone())).collect();
                        (HashMap::new(), Type::Union(results))
                    }

                },
                None => (HashMap::new(), Type::Boolean),
            },
            Schema::Object(sch) => {
                assert!(sch.additional_properties == false);
                let mut all_defs = HashMap::<String, Dataclass>::new();
                let mut fields = HashMap::<String, Field>::new();
                for (k, v) in sch.properties.iter() {
                    let (defs, typ) = parse_dataclass(k, v);
                    all_defs.extend(defs);
                    fields.insert(k.to_string(), Field::new(k, typ, sch.required.contains(k)));
                }
                let c = Dataclass {
                    name: make_class_name(name),
                    subclasses: all_defs,
                    fields,
                };
                (HashMap::from([(make_class_name(name), c)]), Type::TypeName(make_class_name(name)))
            },
        },
        schema::Type::AnyOf(schema::AnyOf { any_of: choices }) => {
            let mut all_defs = HashMap::<String, Dataclass>::new();
            let mut types = Vec::<Type>::new();
            let mut i = 0;
            for v in choices.iter() {
                let k = format!("{}_choice_{}", name, i);
                let (defs, typ) = parse_dataclass(&k, v);
                all_defs.extend(defs);
                types.push(typ);
                i += 1
            }
            (all_defs, Type::Union(types))
        },
        schema::Type::Ref(x) => (HashMap::new(), Type::TypeName(make_class_name(&resolve_ref(&x.ref_id)))),
    }
}

pub struct SchemaPrinter {
    lines: Vec<String>,
    level: usize,
}

impl SchemaPrinter {
    pub fn print(defs: &Defs, main: &Dataclass) -> String {
        let mut printer = SchemaPrinter { lines: vec![], level: 0 };

        // header
        printer.add_line("from dataclasses import dataclass, field".into());
        printer.add_line("from datetime import date".into());
        printer.add_line("from enum import Enum".into());
        printer.add_line("from typing import *".into());
        printer.add_line("from dataclass_wizard import JSONWizard, json_field  # mypy: ignore".into());

        // sort the definitions
        let order = DefsSorter::compute_order(defs);

        // print the definitions in order
        for name in order.iter() {
            let def = defs.definitions.get(name).unwrap();
            printer.run_def(name, def);
        }

        // print the main schema
        printer.run_dataclass(main);

        // return all lines
        printer.lines.join("\n")
    }
    fn run_def(&mut self, name: &str, def: &Def) {
        match def {
            Def::Alias(typ) => self.add_line(format!("{}: TypeAlias = {}", name, typ.get_type_name())),
            Def::Dataclass(dc) => self.run_dataclass(dc),
        }
    }

    fn run_dataclass(&mut self, dataclass: &Dataclass) {
        self.add_line(format!("@dataclass"));
        self.add_line(format!("class {}(JSONWizard):", dataclass.name));
        self.level += 1;

        for (_name, def) in dataclass.subclasses.iter() {
            self.run_dataclass(def);
        }

        // must re-order so required fields come before not-required fields
        self.add_line(format!("# required fields:"));
        for (_key, field) in dataclass.fields.iter() {
            if field.required {
                self.add_line(format!("{}", field));
            }
        }
        self.add_line(format!("# optional fields:"));
        for (_key, field) in dataclass.fields.iter() {
            if !field.required {
                self.add_line(format!("{}", field));
            }
        }

        if dataclass.subclasses.is_empty() && dataclass.fields.is_empty() {
            self.add_line(format!("pass"))
        }

        self.level -= 1;
    }
    fn add_line(&mut self, s: String) {
        let mut s = s;
        s.insert_str(0, "  ".repeat(self.level).as_str());
        self.lines.push(s)
    }
}

#[cfg(test)]
mod test {
    use serde_json::json;
    use super::*;

    #[test]
    fn integer_type() {
        let input = json!(
            {
                "type": "integer"
            }
        );
        let scm: schema::Type = serde_json::from_value(input).unwrap();
        let (defs, typ) = parse_dataclass("top", &scm);
        assert_eq!(defs, HashMap::from([]));
        assert_eq!(typ, Type::Integer);
    }

    #[test]
    fn object_with_integer() {
        let input = json!(
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
        );
        let scm: schema::Type = serde_json::from_value(input).unwrap();
        let (defs, typ) = parse_dataclass("top", &scm);
        assert_eq!(defs, HashMap::from([(
            "Top".into(),
            Dataclass {
                name: "Top".into(),
                subclasses: HashMap::new(),
                fields: HashMap::from([(
                    "hello".to_string(),
                    Field::new("hello", Type::Integer, true)
                )])
            }
        )]));
        assert_eq!(typ, Type::TypeName("Top".into()));
    }

    #[test]
    fn string_enum() {
        let input = json!(
            {
                "type": "string",
                "enum": [
                    "hi",
                    "hello",
                    "bye"
                ]
            }
        );

        let scm: schema::Type = serde_json::from_value(input).unwrap();
        let (defs, typ) = parse_dataclass("top", &scm);
        assert_eq!(defs, HashMap::from([]));
        assert_eq!(typ, Type::Union(vec![
            Type::StringLiteral("hi".into()),
            Type::StringLiteral("hello".into()),
            Type::StringLiteral("bye".into()),
        ]));
    }

    #[test]
    fn string_const() {
        let input = json!(
            {
                "type": "string",
                "const": "hewo"
            }
        );

        let scm: schema::Type = serde_json::from_value(input).unwrap();
        let (defs, typ) = parse_dataclass("top", &scm);
        assert_eq!(defs, HashMap::from([]));
        assert_eq!(typ, Type::StringLiteral("hewo".into()));
    }

    #[test]
    fn array() {
        let input = json!(
            {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        );
        let scm: schema::Type = serde_json::from_value(input).unwrap();
        let (defs, typ) = parse_dataclass("top", &scm);
        assert_eq!(defs, HashMap::from([]));
        assert_eq!(typ, Type::List(Box::new(Type::String)));
    }

    #[test]
    fn complex_array_object() {
        let inner_item = json!(
            {
                "type": "object",
                "additionalProperties": false,
                "properties": {
                    "word": {
                        "type": "string"
                    },
                    "num": {
                        "type": "integer"
                    }
                },
                "required": [
                    "word"
                ]
            }
        );
        let input = json!(
            {
                "type": "object",
                "additionalProperties": false,
                "properties": {
                    "things": {
                        "type": "array",
                        "items": inner_item
                    },
                    "tag": {
                        "type": "string",
                        "enum": [
                            "A",
                            "B"
                        ]
                    }
                },
                "required": [
                    "tag"
                ]
            }
        );
        let scm: schema::Type = serde_json::from_value(input).unwrap();
        let (defs, typ) = parse_dataclass("top", &scm);
        let inner_dataclass = Dataclass {
            name: "Thing".into(),
            subclasses: HashMap::from([]),
            fields: HashMap::from([
                ("word".into(), Field::new("word", Type::String, true)),
                ("num".into(), Field::new("num", Type::Integer, false))
            ])
        };
        assert_eq!(defs, HashMap::from([("Top".into(), Dataclass {
            name: "Top".into(),
            subclasses: HashMap::from([("Thing".into(), inner_dataclass)]),
            fields: HashMap::from([
                ("things".into(), Field::new("things", Type::List(Box::new(Type::TypeName("Thing".into()))), false)),
                ("tag".into(), Field::new("tag", Type::Union(vec![
                    Type::StringLiteral("A".into()),
                    Type::StringLiteral("B".into())
                ]), true))
            ])
        })]));
        assert_eq!(typ, Type::TypeName("Top".into()));
    }
}