// shadowing
fn shadowing() {
    let x = 3;
    println!("x: {x}");
    
    let x = x + 1;
    println!("x: {x}");

    {
        let x = 5;
        println!("x: {x}")
    }
    println!("x: {x}")
}