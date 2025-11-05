"""
to parse a vault dump file and extract a valid SAFE code.
"""
import re
from rooms.base_room import BaseRoom

class VaultCorridorRoom(BaseRoom):
    """
    main room class for the vault corridor room
    """
    def __init__(self):
        """
        initialize the vault corridor room
        """
        super().__init__(
            "VaultCorridor", 
            "A dark corridor full of random SAFE codes. Only one is valid.",
            ["vault_dump.txt"]
             )
        self.safe_regex =  re.compile(r"SAFE\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\}",
                                      re.IGNORECASE)


    def inspect(self, item, player, logger):
        """
        main inspect method for the vault corridor room
        """
        if item != "vault_dump.txt":
            return f"No such item: {item}"
        try:
            with open("data/vault_dump.txt", "r") as f:
                content = f.read()
        except FileNotFoundError:
            return "Error:vault_dump.txt not found in data folder."
        matches = self.safe_regex.findall(content)
        valid_token = None
        for a_str, b_str, c_str in matches:
            a, b, c = int(a_str), int(b_str), int(c_str)
            if a + b == c:
                valid_token = f"SAFE{{{a}-{b}-{c}}}"
                match_str = f"SAFE{{{a}-{b}-{c}}}"
                check_expr = f"{a} + {b} == {c}"
                break

        if valid_token is None:
            return "No valid SAFE code found."

        player.add_token("SAFE", valid_token)
        logger.log(f"valid token found: {valid_token}")
        logger.log(f"Matched string: {match_str}")
        logger.log(f"Validation check: {check_expr}")
        return f"Token extracted: {valid_token}"
            