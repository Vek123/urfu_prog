from typing import Any


class Codec:
    prefix = "https://tinyurl.com"
    alphabet = (
        "abcdefghijklmnopqrstuvwxyzABCDEF"
        "GHIJKLMNOPQRSTUVWXYZ0123456789"
    )

    def __init__(self) -> None:
        self.db: dict[int, dict[str, Any]] = {}

    def _encode_id(self, n: int) -> str:
        short_url = ""
        while n:
            short_url += self.alphabet[n % 62]
            n //= len(self.alphabet)
    
        return short_url[::-1]

    def _decode_id(self, s: str) -> int:
        n = 0
  
        for i in s:
            if "a" <= i and i <= "z":
                n = n*62 + ord(i) - ord("a")
            elif "A" <= i and i <= "Z":
                n = n*62 + ord(i) - ord("A") + 26
            elif "0" <= i and i <= "9":
                n = n*62 + ord(i) - ord("0") + 52

        return n

    def _get_last_id(self) -> int:
        return list(self.db.keys())[-1] if self.db else 0

    def encode(self, longUrl: str) -> str:
        """Encodes a URL to a shortened URL.
        """

        n = self._get_last_id() + 1
        short_url = self._encode_id(n)
        self.db[n] = {"original_url": longUrl, "short_url": short_url}
        return self.prefix + "/" + short_url

    def decode(self, shortUrl: str) -> str:
        """Decodes a shortened URL to its original URL.
        """

        data = shortUrl.lstrip("https://")
        data = data[data.find("/")+1:]
        n = self._decode_id(data)
        return self.db[n]["original_url"]
