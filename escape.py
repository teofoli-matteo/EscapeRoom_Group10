"""Main entry point for the Cyber Escape Room game."""
import argparse
from engine.game import Game

def main():
    """Parse command-line arguments and start the game."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="intro", )
    parser.add_argument("--transcript", default="run.txt", help="Transcript file")
    args = parser.parse_args()

    game = Game(starting_room=args.start, transcript="run.txt")
    game.run()

if __name__ == "__main__":
    main()
