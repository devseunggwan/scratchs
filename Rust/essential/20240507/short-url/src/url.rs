use base32;
use sha2::{Digest, Sha256};

pub fn digest(url: &str) -> Vec<u8> {
    let mut hasher = Sha256::new();
    hasher.update(url.as_bytes());
    hasher.finalize().to_vec()
}

pub fn truncated_base32(digest: &Vec<u8>, truncate_len: usize) -> String {
    let truncated: &[u8] = &digest.as_slice()[..truncate_len];
    base32::encode(base32::Alphabet::Crockford, truncated)
}

pub fn base32_normalize(encoded: &str) -> Option<String> {
    let decoded = base32::decode(base32::Alphabet::Crockford, encoded)?;
    Some(base32::encode(base32::Alphabet::Crockford, &decoded))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_digest() {
        let a_long_url = "https://www.naver.com";
        let b_long_url = "https://www.google.com";
        let a_digest = digest(a_long_url);
        assert_eq!(32, a_digest.len());
        assert_eq!(a_digest, digest(a_long_url));
        assert_ne!(a_digest, digest(b_long_url));
    }

    #[test]
    fn test_base32() {
        let data = digest("https://long-url");
        let base32 = truncated_base32(&data, 2);
        assert_eq!(base32.len(), 4);
        assert_eq!("CGF0", base32);
    }

    #[test]
    fn test_base32_normalize() {
        assert_eq!("CGF0", base32_normalize("CGFO").unwrap());
        assert_eq!("1111A", base32_normalize("1ilIA").unwrap());
    }

}
