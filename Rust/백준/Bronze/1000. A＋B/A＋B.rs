use std::io::stdin;

fn main() {
    let mut buffer: String = String::new();
    stdin().read_line(&mut buffer).unwrap();

    let mut iter  = buffer.trim().split_whitespace();
    let a: i32 = iter.next().unwrap().parse::<i32>().unwrap();
    let b: i32 = iter.next().unwrap().parse::<i32>().unwrap();

    println!("{}", a + b);
}