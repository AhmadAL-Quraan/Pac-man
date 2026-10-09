import sys
from config import Config
from game_system.game import Game


def main() -> None:
    """Entry point: load config and start the game."""
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config.json>")
        sys.exit(1)

    try:
        config = Config.load(sys.argv[1])
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Loaded config from {sys.argv[1]}")

    try:
        game = Game(config)
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected fatal error occurred: {e}")
        sys.exit(1)
