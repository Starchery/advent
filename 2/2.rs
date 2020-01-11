/* Advent of Code */
use std::fs;
use std::cell::Cell;

fn main() {
    let intcode = convert_program(&fs::read_to_string("input")
                                        .expect("Failed to read")
                                        .trim()
                                     );
    let new_program = run(&intcode);
    println!("{:?}", new_program[0].get());
}

fn convert_program(program: &str) -> Vec<Vec<Cell<usize>>> {
    let mut table: Vec<Vec<Cell<usize>>> = Vec::new();
    for elem in program.split(",").collect::<Vec<_>>().chunks(4) {
        table.push(
            elem.iter().map(|x| 
                Cell::new(x.parse::<usize>().expect("Failed to parse"))
            ).collect()
        )
    }
    table
}

fn run(program: &Vec<Vec<Cell<usize>>>) -> Vec<Cell<usize>> {
    let mut prog = program.to_vec().into_iter().flatten().collect::<Vec<Cell<usize>>>();
    for directive in program.into_iter() {
        match (directive[0]).get() {
            1 => {
                prog[directive[3].get()] = Cell::new(prog[directive[1].get()].get() 
                                                   + prog[directive[2].get()].get())
            },
            2 => {
                prog[directive[3].get()] = Cell::new(prog[directive[1].get()].get() 
                                                   * prog[directive[2].get()].get())
            },
            _ => break
        }
    }
    prog
}


/*
-  0 1 2 3 
 ---------
0| 0 1 2 3
1| 7 8 9 0
2| 1 2 3 4
3| 5 6 7 8
4| 9 0 1 2
5| 3 4 5 6
6| 7 8 9 0
*/