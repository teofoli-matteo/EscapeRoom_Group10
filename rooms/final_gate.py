from __future__ import annotations
from .base_room import BaseRoom
from typing import Dict, Optional, Tuple, Any


class FinalRoom(BaseRoom):

    def __init__(self) -> None:
        super().__init__(
            "Final Gate",
            "The final gate checks cryptographic integrity of tokens. Use the gate to submit proof.",
            []
        )

    def _parse_final_file(self, path: str = "data/final_gate.txt") -> Tuple[Optional[Dict[str, str]], Optional[str]]:
        """
        Parse the final gate configuration file.
        Args:path: Path to the final_gate.txt configuration file.
        Returns: A tuple . If parsing fails, config_dict is None and error_message is set.
        """
        conf: Dict[str, str] = {}
        try:
            with open(path, "r") as f:
                for raw in f:
                    line = raw.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    k, v = map(str.strip, line.split("=", 1))
                    conf[k] = v
        except FileNotFoundError:
            return None, "final_gate.txt not found."

        return conf, None

    def use(self, item: str, player: Any, logger: Any) -> str:
        """
        Use an item in the Final Gate room (use gate).
        Reads the final_gate.txt file, retrieves required tokens from the player inventory, and logs the message and expected HMAC for instructor verification.
        Args: item: The item name ("gate"). player: The Player instance holding collected tokens. logger: The Logger instance for transcript recording.
        Return: A descriptive string about the gate processing result.
        """
        logger.log("[Room Final] Reading final_gate.txt...")

        conf, err = self._parse_final_file()
        if err:
            return err

        id_grp = conf.get("group_id")
        hmac = conf.get("expected_hmac")
        token_order = conf.get("token_order")

        if not id_grp or not hmac or not token_order:
            return "final_gate.txt is missing required fields."

        token_keys = [k.strip() for k in token_order.split(",") if k.strip()]
        token_values: list[str] = []
        missing: list[str] = []

        for key in token_keys:
            value = player.inventory.get(key)
            if value is None:
                token_values.append("?")
                missing.append(key)
            else:
                token_values.append(value)

        msg = f"{id_grp}|{'-'.join(token_values)}"

        logger.log("FINAL_GATE=PENDING")
        logger.log(f"MSG={msg}")
        logger.log(f"EXPECTED_HMAC={hmac}")

        if missing:
            logger.log(f"[Room Final] WARNING: missing tokens for keys: {', '.join(missing)}")
            return (
                f"Gate processed but tokens missing: {', '.join(missing)}. "
                "Transcript written. FINAL_GATE=PENDING"
            )

        return "Gate processed. FINAL_GATE=PENDING. Transcript written."
