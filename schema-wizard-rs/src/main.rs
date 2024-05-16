use serde_json::json;

pub mod schema;
pub mod dataclass;

fn main() {
    let input = std::fs::read_to_string("assets/mnx-schema.json").unwrap();
    let top: schema::Type = serde_json::from_str(&input).unwrap();
    let (defs, typ) = dataclass::parse("top", &top);
    let s = dataclass::DataclassPrinter::print(defs.get("Top").unwrap());
    println!("{}", s)
}
