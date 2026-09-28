from json import load
import sys
from config import Config


def start():
    if len(sys.argv) != 2:
        print("Error, 2 argument only allowed")
        sys.exit(1)

    try:
        config = Config.load("config.json")
    except Exception as e:
        print(f"(Error happened) {e}")


start()
