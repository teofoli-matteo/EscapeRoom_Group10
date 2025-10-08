from .base_room import BaseRoom

class Lobby(BaseRoom):
    def __init__(self):
        super().__init__(
            "Lobby",
            "A terminal blinks in the corner. Doors lead to: soc, dns, vault, malware, final."
        )

    def look(self):
        return (
            "You are in the Intro Lobby.\n"
            "A terminal blinks in the corner. Doors lead to: soc, dns, vault, malware, final"
        )