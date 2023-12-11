fn main() {
    let reader = std::io::stdin();
    let mut buf = String::new();
    let _ = reader.read_line(&mut buf).expect("read failed");
    let flag = buf.trim().as_bytes();
    if flag.len() == 10 {
        if flag[0] != b'f'
            || flag[1] != b'l'
            || flag[2] != b'a'
            || flag[3] != b'g'
            || flag[4] != b'{'
            || flag[9] != b'}'
        {
            return;
        }
        let (a, b, c, d) = (flag[5], flag[6], flag[7], flag[8]);
        if !(a + b == 227 && b - c == 11 && c as u16 * d as u16 == 11100 && a - d == 5) {
            return;
        }
        println!("OK");
    }
}
