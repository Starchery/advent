/* Advent of Code */
use std::fs;

fn main() {
	let intcode = convert_program(&fs::read_to_string("input")
				      			    .expect("Failed to read")
				      			    .trim()
					      		 );
	let matrix = run(&intcode);
	println!("{:?}", matrix);
}

fn run(program: &Vec<Vec<usize>>) -> Vec<usize> {
	let mut matrix: Vec<usize> = Vec::new();
	for directive in program {
		match update(&directive, &matrix) {
			Some(value) => matrix = value,
			_ => break
		}
	}
	matrix
}

fn convert_program(program: &str) -> Vec<Vec<usize>> {
	let mut table: Vec<Vec<usize>> = Vec::new();
	for elem in program.split(",").collect::<Vec<_>>().chunks(4) {
		table.push(
			elem.iter().map(|x| 
				x.parse::<usize>().expect("Failed to parse")
			).collect()
		)
	}
	table
}

fn update(directive: &Vec<usize>, matrix: &Vec<usize>) -> Option<Vec<usize>> {
	let mut program = matrix.to_vec();
	for elem in directive {
		program.push(*elem)
	}

	match directive.get(0) {
		Some(1) => {
			program.remove(directive[3]);
			program.insert(directive[3], 
				program[directive[1]] + program[directive[2]])
		},
		Some(2) => {
			program.remove(directive[3]);
			program.insert(directive[3], 
				program[directive[1]] * program[directive[2]])
		},
		_ => return None
	}

	Some(program)
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