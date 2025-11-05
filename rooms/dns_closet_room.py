"""
dns_closet_room.py:
Decode DNS hints and recover the DNS token.
"""
import base64
from rooms.base_room import BaseRoom

class DnsClosetRoom(BaseRoom):
    """Room logic for decoding DNS hints."""
    def __init__(self):
        super().__init__(
            "Dns Closet",
            "The walls are covered with scribbled key=value pairs.",
            ["dns.cfg"]
        )

    def _safe_b64decode(self, val: str) -> str:
        """Decode Base64 while tolerating padding/newline issues."""
        val = val.replace("\\\n", "").strip()

        missing = len(val) % 4
        if missing:
            val += "=" * (4 - missing)

        try:
            return base64.b64decode(val).decode("utf-8", errors="ignore")
        except Exception:
            return None

    def inspect(self, item, player, logger):
        """
        Inspect the given item and extract a token from a DNS zone fragment.

        Args:
            item (str): The name of the item to inspect (dns.cfg).
            player (Player): The player instance to store the token in.
            logger (Logger): The logger instance for recording actions.

        Returns:
            str: A message indicating the result of the inspection.
        """
        if item != "dns.cfg":
            return f"No such item: {item}."

        logger.log("[Room DNS] Decoding hints...")

        try:
            with open("./data/dns.cfg", encoding="UTF-8") as file:
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
