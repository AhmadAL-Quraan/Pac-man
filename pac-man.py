import sys
from config import Config
from game_system.game import Game


def main() -> None:
    """Entry point: load config and start the game."""
    config_path: str = ""
    print()
    if len(sys.argv) != 2:
        print(
            f"Program only takes 1 arguments which is the configuration file"
        )
        sys.exit(-1)

    config_path = sys.argv[1]

    try:
        config = Config.load(config_path)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Loaded config from {config_path}")

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
