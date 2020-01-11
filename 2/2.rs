/* Advent of Code */
use std::cell::Cell; // required to internally mutate a collection mid-traversal
use std::env;
use std::fs;

fn main() {
    let terminal = match env::args().collect::<Vec<String>>().get(1) {
        Some(x) => x.parse::<usize>().unwrap(),
        None => 19_690_720usize, // if an argument is supplied, use it as the terminal value.
    }; // otherwise, use the default value of 19690720

    match values_that_produce(
        terminal,
        fs::read_to_string("input").unwrap().trim().to_string(),
    ) {
        Some((x, y)) => println!("x: {} y: {}\n{:?}", x, y, (100 * x) + y),
        None => println!("No combination exists that produces {}", terminal),
    }
}

fn values_that_produce(term: usize, data: String) -> Option<(usize, usize)> {
    for i in 0..100 {
        // brute forces every combination of (x, y)
        for j in 0..100 {
            let intcode = run(&convert_program(&data, (i, j)));
            if intcode[0].get() == term {
                // if the output from running the program
                return Some((i, j)); // is the terminal value, return the values
            } // used to create it
        }
    }
    None
}

fn convert_program(program: &str, args: (usize, usize)) -> Vec<Vec<Cell<usize>>> {
    let mut table: Vec<Vec<Cell<usize>>> = Vec::new();
    for elem in program.split(",").collect::<Vec<_>>().chunks(4) {
        // split by program
        table.push(
            // each program is 4 elements [opcode pos1 pos2 destination]
            elem.iter()
                .map(|x| Cell::new(x.parse::<usize>().expect("Failed to parse")))
                .collect(),
        )
    }
    table[0][1] = Cell::new(args.0); // replace values in 1th and 2th positions
    table[0][2] = Cell::new(args.1); // with test values, as instructed
    table
}

fn run(program: &Vec<Vec<Cell<usize>>>) -> Vec<Cell<usize>> {
    let mut prog = program // collapse two-dimensional vector into
        .to_vec() // one-dimensional to simplify the lookup process
        .into_iter() // while changing values in the program
        .flatten()
        .collect::<Vec<Cell<usize>>>();
    for dir in program.into_iter() {
        match (dir[0]).get() {
            1 => {
                // addition: replace value in pos_3 with the sum of values in pos_1 and pos_2
                prog[dir[3].get()] = Cell::new(prog[dir[1].get()].get() + prog[dir[2].get()].get())
            }
            2 => {
                // multiplication: replace value in pos_3 with the product of values in pos_1 and pos_2
                prog[dir[3].get()] = Cell::new(prog[dir[1].get()].get() * prog[dir[2].get()].get())
            }
            _ => break, // a code of 99 or any other unrecognized code halts the program immediately.
        }
    }
    prog
}
