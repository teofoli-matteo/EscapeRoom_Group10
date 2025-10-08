import sys

from engine.player import Player
from rooms.lobby import Lobby
from rooms.soc_triage import SocTriageRoom

class Game:
    def __init__(self, starting_room="baseroom"):
        self.rooms = {
            "intro": Lobby(),
            "soc": SocTriageRoom()
        }
        self.current_room = self.rooms.get(starting_room, Lobby())
        self.player = Player()
        
    def run(self):
        print("[Game] Cyber Escape Room started. Type 'help' for commands.")
        while True:
            try:
                cmd = input("> ").strip().split()
                if not cmd:
                    continue
                action, *args = cmd
                if action == "quit":
                    print("[Game] Goodbye. Transcript written to transcript.txt")
                    sys.exit(0)
                elif action == "help":
                    print("Commands: look, move <room>, inspect <item>, use <item>, inventory, save, hint, quit")
                elif action == "look": print(self.current_room.look())
                elif action == "move":
                    if args:
                        destination = args[0]
                        if destination in self.rooms:
                            self.current_room = self.rooms[destination]
                            print(self.current_room.enter())
                        else:
                            print("Where are you going ?")
                elif action == 'inventory': print(self.player.show_inventory())
                else:
                    print("Unknown command.")
            except KeyboardInterrupt:
                print("\n[Game] Interrupted. Exiting.")
                sys.exit(0)