import re
from .base_room import BaseRoom

class SocTriageRoom(BaseRoom):
    def __init__(self):
        """Initialize the SOC triage room with its name, description, and items."""
        super().__init__(
            "SOC Triage Desk",
            "A cluttered screen shows failed SSH login attempts.",
            ["auth.log"]
        )

    def inspect(self, item, player, logger):
        """
        Inspect the given item and extract a token from SSH authentication logs.

        Args:
            item (str): The name of the item to inspect (auth.log).
            player (Player): The player instance to store the token in.
            logger (Logger): The logger instance for recording actions.

        Returns:
            str: A message indicating the result of the inspection.
        """
        if item != "auth.log":
            return f"No item named: {item}"
        logger.log("[Room SOC] Parsing auth.log...")
        try:
            with open("data/auth.log", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            return ("auth.log file is missing.")
        failures_by_subnet = {}
        malformed_lines = 0
        sample_line = None
        for line in lines:
            try:
                if "Failed password" in line:
                    message = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
                    if message:
                        ip = message.group(1)
                        parts = ip.split(".")
                        subnet = ".".join(parts[:3]) + ".0/24"
                        if subnet not in failures_by_subnet:
                            failures_by_subnet[subnet] = {}
                        failures_by_subnet[subnet][ip] = failures_by_subnet[subnet].get(ip, 0) + 1
                        if not sample_line:
                            sample_line = line.strip()
                    else:
                        malformed_lines +=1
                else:
                    continue
            except Exception as exc:
                print(f"[Room SOC] Error parsing line: {exc}")
                malformed_lines += 1
        if not failures_by_subnet:
            return "No failed login attempts found."
        subnet_counts = {s: sum(ip_counts.values()) for s, ip_counts in failures_by_subnet.items()}
        top_subnet = max(subnet_counts, key=subnet_counts.get)
        top_count = subnet_counts[top_subnet]
        top_ip = max(failures_by_subnet[top_subnet], key=failures_by_subnet[top_subnet].get)
        last_octet = top_ip.split(".")[-1]
        token_value = f"{last_octet}{top_count}"
        player.add_token("KEYPAD", token_value)
        logger.log(f"{top_count} failed attempts found in {top_subnet}")
        logger.log(f"Top IP is {top_ip} (last octet={last_octet})")
        logger.log(f"Token formed: {token_value}")
        logger.log(f"TOKEN[KEYPAD]={token_value}")
        logger.log(f"EVIDENCE[KEYPAD].TOP24={top_subnet}")
        logger.log(f"EVIDENCE[KEYPAD].COUNT={top_count}")
        if sample_line:
            logger.log(f"EVIDENCE[KEYPAD].SAMPLE={sample_line}")
        logger.log(f"EVIDENCE[KEYPAD].MALFORMED_SKIPPED={malformed_lines}")
        return f"token: {token_value}"