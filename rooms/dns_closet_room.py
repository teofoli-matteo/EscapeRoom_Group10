from .base_room import BaseRoom

import base64

class DnsClosetRoom(BaseRoom):
    def __init__(self):
        super().__init__(
            "Dns Closet",
            "The walls are covered with scribbled key=value pairs.",
            ["dns.cfg"]
        )

    def _safe_b64decode(self, val: str) -> str:
        val = val.replace("\\\n", "").strip()

        missing = len(val) % 4
        if missing:
            val += "=" * (4 - missing)

        try:
            return base64.b64decode(val).decode("utf-8", errors="ignore")
        except Exception:
            return None

    def inspect(self, item, player, logger):
        if item != "dns.cfg":
            return f"No such item: {item}."
        
        logger.log("[Room DNS] Decoding hints...")
        
        try:
            with open("./data/dns.cfg") as file:
                lines = file.readlines()
        except FileNotFoundError:
            return '"dns.cfg" can not be found.'
        
        token_key = None
        hints = {}

        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue

            key, value = map(str.strip, line.split("=", 1))

            if key == "token_tag":
                str_decode = self._safe_b64decode(value)
                token_key = str_decode if str_decode else value

                if str_decode.isdigit():
                    token_key = f"hint{str_decode}"
                continue

            if key.startswith("hint"):
                str_decode = self._safe_b64decode(value)
                if str_decode:
                    hints[key] = str_decode

        if not token_key or token_key not in hints:
            return "No valid token found in dns.cfg."
        
        decoded_line = hints[token_key].strip()
        token_word = decoded_line.split()[-1]

        player.add_token("DNS", token_word)

        logger.log(f'Decoded line: "{decoded_line}"')
        logger.log(f"Token formed: {token_word}")
        logger.log(f"TOKEN[DNS]={token_word}")
        logger.log(f"EVIDENCE[DNS].KEY={token_key}")
        logger.log(f"EVIDENCE[DNS].DECODED_LINE={decoded_line}")

        return f"Token extracted: {token_word}"