// 데이터 타입
// Rust에서 모든 값은 특정 데이터의 타입 값
// 기본값 Scalar, 복합값 Compound
// Rust는 정적 타입 언어
// 컴파일 시점에 모든 변수의 타입을 알아야 합니다.

let x = 3.14; // f64
let y: f32 = 3.14; // f32

let add = 5 + 10; // i32
let sub = 95.5 - 4.3; // f64
let mul = 4 * 30; // i32
let div = 56.7 / 32.2; // f64
let truncated = 43 / 5; // i32 (7)
let rem = 43 % 5; // i32

let t = true;
let f: bool = false;

let c = 'z';
let z: char = 'ℤ';
let heart_eyed_cat = '😻';