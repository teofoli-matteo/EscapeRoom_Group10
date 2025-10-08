from .base_room import BaseRoom

class SocTriageRoom(BaseRoom):
    def __init__(self):
        super().__init__(
            "SOC Triage Desk",
            "A cluttered screen shows failed SSH login attempts.",
            ["auth.log"]
        )

   