import argparse
from engine.game import Game

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="intro")
    args = parser.parse_args()

    game = Game(starting_room=args.start)
    game.run()

if __name__ == "__main__":
    main()
