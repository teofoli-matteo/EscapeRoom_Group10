from .base_room import BaseRoom
import re

class VaultCorridorRoom(BaseRoom):
    def __init__(self):
        super().__init__(
            "VaultCorridor", 
            "A dark corridor full of random SAFE codes. Only one is valid."
            ["Vault_dump.txt"]
             )
        
        self.safe_regex
        re.compile(r'SAFE\{\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\}')
        
        def inspect(self, item, player, logger):
            if item != "vault_dump.txt": 
                return f"No such item: {item}"
            
            try:
                with open("data/vault_dump.txt", "r")
                content = f.read()
            except FileNotFoundError:
                return "Error:vault_dump.txt not found in data folder."
            
            matches = self.safe_regex.findall(content)
            
            valid_token = None
            
            for match in matches:
                a, b, c = int(match[0]),
                int(match[1]), int(match[2])
                
                if a + b == c:
                    valid_token = 
                    f"SAFE{{{a}--{b}--{c}}}"
                    match_str =
                    f"SAFE{{{a}--{b}--{c}}}"
                    check_expr = f"{a} + {b} == {c}"
                    break
                
                if valid_token is None:
                    return "No valid SAFE code found."
                
                player.add_token("SAFE", valid_token)
                
                logger.info(f"valid token found: {Valid_token}")
                logger.info(f"Matched string: {match_str}")
                logger.info(f"Validation check: {check_expr}")
                
                return f"Token extracted: {valid_token}"
            
            