"""
game.py
Main game engine for the Cyber Escape Room project.
Manages rooms, player state, logging, and user interaction loop.
"""

import sys
import json

from engine.player import Player
from engine.logger import Logger
from rooms.lobby import Lobby
from rooms.soc_triage import SocTriageRoom
from rooms.dns_closet_room import DnsClosetRoom
from rooms.vault_corridor_room import VaultCorridorRoom
from rooms.malware_room import MalwareLabRoom
from rooms.final_gate import FinalRoom


class Game:
    """Main game class that manages player interactions and room transitions."""

    def __init__(self, starting_room: str = "intro", transcript: str = "run.txt") -> None:
        """
        Initialize the game environment.

        Args:
            starting_room (str): The name of the starting room.
            transcript (str): File to store the transcript log.
        """
        self.rooms = {
            "intro": Lobby(),
            "soc": SocTriageRoom(),
            "dns": DnsClosetRoom(),
            "vault": VaultCorridorRoom(),
            "malware": MalwareLabRoom(),
            "final": FinalRoom(),
        }
        self.current_room = self.rooms.get(starting_room, Lobby())
        self.player = Player()
        self.logger = Logger(transcript)

    def run(self) -> None:
        """Main game loop handling user input and actions."""
        print("[Game] Cyber Escape Room started. Type 'help' for commands.")

        while True:
            try:
                cmd = input("> ").strip().split()
                if not cmd:
                    continue

                action, *args = cmd

                if action == "quit":
                    print("[Game] Goodbye. Transcript written to run.txt")
                    self.logger.save()
                    sys.exit(0)

                if action == "help":
                    print(
                        "Commands: look, move <room>, inspect <item>, use <item>, "
                        "inventory, save <file>, load <file>, quit"
                    )
                    continue

                if action == "look":
                    print(self.current_room.look())
                    continue

                if action == "move":
                    self._handle_move(args)
                    continue

                if action == "inventory":
                    print(self.player.show_inventory())
                    continue

                if action == "inspect":
                    self._handle_inspect(args)
                    continue

                if action == "save":
                    self._handle_save(args)
                    continue

                if action == "load":
                    self._handle_load(args)
                    continue

                if action == "use":
                    self._handle_use(args)
                    continue
                
                if action == "hint":
                    self._handle_hint()
                    continue

                print("Unknown command.")

            except KeyboardInterrupt:
                print("\n[Game] Interrupted. Exiting.")
                self.logger.save()
                sys.exit(0)

    def _handle_move(self, args: list[str]) -> None:
        """Handle room transition commands."""
        if not args:
            print("Specify room to move to.")
            return

        destination = args[0]
        if destination in self.rooms:
            self.current_room = self.rooms[destination]
            print(self.current_room.enter())
        else:
            print("Where are you going?")

    def _handle_inspect(self, args: list[str]) -> None:
        """Handle inspecting items within a room."""
        if not args:
            print("Inspect what?")
            return
        print(self.current_room.inspect(args[0], self.player, self.logger))

    def _handle_use(self, args: list[str]) -> None:
        """Handle using an item in a room."""
        if not args:
            print("Use what?")
            return
        print(self.current_room.use(args[0], self.player, self.logger))

    def _handle_save(self, args: list[str]) -> None:
        """Handle saving player progress."""
        if not args:
            print("Specify filename to save.")
            return

        filename = args[0]
        state = {
            "current_room": self.current_room.name,
            "inventory": self.player.inventory,
        }
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(state, file, indent=4)
            print("[Game] Progress saved.")
        except OSError as err:
            print(f"[Game] Failed to save: {err}")

    def _handle_load(self, args: list[str]) -> None:
        """Handle loading previously saved progress."""
        if not args:
            print("Specify filename to load.")
            return

        filename = args[0]
        try:
            with open(filename, "r", encoding="utf-8") as file:
                state = json.load(file)
            room_name = state.get("current_room", "intro")
            self.current_room = self.rooms.get(room_name, Lobby())
            self.player.inventory = state.get("inventory", {})
            print(f"[Game] Progress loaded from {filename}.")
        except FileNotFoundError:
            print(f"[Game] Save file not found: {filename}")
        except (OSError, json.JSONDecodeError) as err:
            print(f"[Game] Failed to load: {err}")
            
    def _handle_hint(self) -> None:
        """
        Handle the 'hint' command.
        """
        room_name = getattr(self.current_room, 'name', "").lower()

        if room_name == "final gate":
            print("[Hint] to attempt to open the gate, use : use gate")
            return

        rooms_items = getattr(self.current_room, "items", [])
        if rooms_items:
            print(f"[Hint] Try inspecting the items in this room: {', '.join(rooms_items)}")
        else:
            print("[Hint] There is nothing here.")
