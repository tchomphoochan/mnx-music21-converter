pub mod schema;
pub mod dataclass;

use clap::Parser;

#[derive(Parser, Debug)]
pub struct Args {
    #[clap(short = 'i', long, value_name = "input")]
    pub input: Option<std::path::PathBuf>,

    #[clap(short = 'o', long, value_name = "output")]
    pub output: Option<std::path::PathBuf>,
}

fn get_reader(input: &Option<std::path::PathBuf>) -> Box<dyn std::io::Read> {
    match input {
        Some(path) => Box::new(std::fs::File::open(path.as_path()).unwrap()),
        None => Box::new(std::io::stdin())
    }
}
fn get_writer(output: &Option<std::path::PathBuf>) -> Box<dyn std::io::Write> {
    match output {
        Some(path) => Box::new(std::fs::File::create(path.as_path()).unwrap()),
        None => Box::new(std::io::stdout())
    }
}

fn main() {
    let args = Args::parse();
    let mut infile = get_reader(&args.input);
    let mut outfile = get_writer(&args.output);

    let mut input = String::new();
    infile.read_to_string(&mut input).unwrap();

    let top: schema::TopLevel = serde_json::from_str(&input).unwrap();
    let (defs, _typ) = dataclass::parse("top", &top.content);
    let s = dataclass::DataclassPrinter::print(defs.get("Top").unwrap());
    write!(outfile, "{}", s).unwrap();
}
