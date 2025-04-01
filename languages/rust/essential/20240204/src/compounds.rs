
// tuple
// 서로 다른 타입 여러개 관리
let t: (i32, f64, u8) = (500, 6.4, 1);
let (x, y, z) = t;

let x =  t.0;
let y = t.1;
let z = t.2;

// array
// 동일한 타입만 여러개 관리
// 길이가 고정
let a = [1, 2, 3, 4, 5];
let a: [i32; 5] = [1, 2, 3, 4, 5];
let first = a[0];
let second = a[1];

let a = [3; 5]; // [3, 3, 3, 3, 3]

