/* Advent of Code */
use std::fs;

fn main() {
    let data = fs::read_to_string("input").expect("Failed to read file");
    let mod_fuel: Vec<f64> = data.lines() // split by '\n'
                                 .map(|x| // convert masses to their fuels
                                     extra_fuel(x.parse::<f64>().unwrap())
                                 )
                                 .collect();

    let total_fuel: f64 = mod_fuel.iter().sum();
    println!("{:?}", total_fuel);
}

fn calculate_fuel(module: f64) -> f64 {
    (module / 3.0).trunc() - 2.0
}

fn extra_fuel(fuel: f64) -> f64 {
    if calculate_fuel(fuel) <= 0.0 {
        0.0
    } else {
        calculate_fuel(fuel) + extra_fuel(calculate_fuel(fuel))
    }
}