import json
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Config:

    lives: int
    seed: int
    level_max_time: int
    points_per_ghost: int
    highscore_filename: str
    points_per_super_pacgum: int
    points_per_pacgum: int
    pacgum: int
    levels_hight_width: list[dict[str, int]]

    DEFAULT_LEVEL: ClassVar[dict[str, int]] = {"width": 21, "height": 21}
    MIN_LEVEL_COUNT: ClassVar[int] = 10
    MIN_DIMENSION: ClassVar[int] = 11
    # 32 pixels
    CELL_SIZE: ClassVar[int] = 32
    SCREEN_WIDTH: ClassVar[int] = 800
    SCREEN_HEIGHT: ClassVar[int] = 800

    MAX_WIDTH: ClassVar[int] = SCREEN_WIDTH // CELL_SIZE
    MAX_HEIGHT: ClassVar[int] = SCREEN_HEIGHT // CELL_SIZE

    @staticmethod
    def _clean_data(raw_text: str) -> str:
        lines = []
        for i in raw_text.splitlines():
            j = i.strip()
            if j.startswith("#") or j.startswith("//") or j == "":
                continue
            lines.append(j)

        return "\n".join(lines)

    @staticmethod
    def _validate_int(raw_dict: dict, key: str, default: int) -> int:
        value = raw_dict.get(key, default)
        if not isinstance(value, int) or isinstance(value, bool):
            print(
                f"Warning: '{key}' must be an integer, using default {default}"
            )
            return default
        return value

    @staticmethod
    def _validate_positive_int(data: dict, key: str, default: int) -> int:
        num = Config._validate_int(data, key, default)
        if num <= 0:
            print(
                f"Warning: '{key}'={num} must be a positive integer, "
                f"using default {default}"
            )
            return default
        return num

    @staticmethod
    def _validate_dimension(value: object, key: str, index: int) -> int:
        """Validate a single width or height value for one level entry.

        Args:
            value: The raw value pulled from the level dict.
            key: "width" or "height", used only for warning messages.
            index: The level's position in the list, used only for warnings.

        Returns:
            A safe, odd, minimum-bounded integer dimension.
        """
        default = Config.DEFAULT_LEVEL[key]
        max_value = Config.MAX_WIDTH if key == "width" else Config.MAX_HEIGHT

        if not isinstance(value, int) or isinstance(value, bool):
            print(
                f"Warning: level {index} '{key}' must be an integer, "
                f"using default {default}"
            )
            return default

        if value < Config.MIN_DIMENSION:
            print(
                f"Warning: level {index} '{key}'={value} too small, "
                f"clamping to {Config.MIN_DIMENSION}"
            )
            value = Config.MIN_DIMENSION

        if value > max_value:
            print(
                f"Warning: level {index} '{key}'={value} too large to fit "
                f"the screen, clamping to {max_value}"
            )
            value = max_value

        return value

    @staticmethod
    def _validate_levels(raw_levels: object) -> list[dict[str, int]]:
        """Validate the 'level' array from a config file.

        Ensures the result is a list of at least MIN_LEVEL_COUNT dicts,
        each with valid, odd, minimum-bounded 'width' and 'height' ints.
        Any missing or malformed entry is replaced with a safe default
        rather than rejecting the whole config.

        Args:
            raw_levels: Whatever raw_dict.get("level") returned — could be
                anything, since it comes straight from untrusted JSON.

        Returns:
            A cleaned list of level dicts, safe to pass to the maze loader.
        """
        if not isinstance(raw_levels, list) or len(raw_levels) == 0:
            print(
                f"Warning: 'level' must be a non-empty list, "
                f"using {Config.MIN_LEVEL_COUNT} default levels"
            )
            return [
                dict(Config.DEFAULT_LEVEL)
                for _ in range(Config.MIN_LEVEL_COUNT)
            ]

        cleaned: list[dict[str, int]] = []
        for i, entry in enumerate(raw_levels):
            if not isinstance(entry, dict):
                print(f"Warning: level {i} is not an object, using default")
                cleaned.append(dict(Config.DEFAULT_LEVEL))
                continue

            cleaned.append(
                {
                    "width": Config._validate_dimension(
                        entry.get("width"), "width", i
                    ),
                    "height": Config._validate_dimension(
                        entry.get("height"), "height", i
                    ),
                }
            )

        while len(cleaned) < Config.MIN_LEVEL_COUNT:
            print(
                f"Warning: only {len(cleaned)} levels provided, "
                f"padding with default levels to reach {Config.MIN_LEVEL_COUNT}"
            )
            cleaned.append(dict(Config.DEFAULT_LEVEL))

        return cleaned

    @staticmethod
    def _validate_str(data: dict, key: str, default: str) -> str:
        filename = data.get(key, default)
        if not isinstance(filename, str) or filename == "":
            print(
                f"Warning: '{key}' must be a non-empty string, "
                f"using default {default!r}"
            )
            return default
        return filename

    @classmethod
    def load(cls, filepath: str) -> "Config":
        try:
            with open(filepath, "r") as file:
                raw_text = file.read()
        except OSError as e:
            raise ValueError(f"Could not read config file: {e}") from e

        cleaned_data = cls._clean_data(raw_text)

        try:
            raw_dict = json.loads(cleaned_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}") from e

        if not isinstance(raw_dict, dict):
            print("Warning: config root must be an object, using all defaults")
            raw_dict = {}

        return cls(
            highscore_filename=Config._validate_str(
                raw_dict, "highscore_filename", "highscores.json"
            ),
            points_per_super_pacgum=Config._validate_positive_int(
                raw_dict, "points_per_super_pacgum", 50
            ),
            points_per_pacgum=Config._validate_positive_int(
                raw_dict, "points_per_pacgum", 10
            ),
            levels_hight_width=Config._validate_levels(raw_dict.get("level")),
            lives=Config._validate_positive_int(raw_dict, "lives", 3),
            seed=Config._validate_positive_int(raw_dict, "seed", 42),
            level_max_time=Config._validate_positive_int(
                raw_dict, "level_max_time", 90
            ),
            pacgum=Config._validate_positive_int(raw_dict, "pacgum", 42),
            points_per_ghost=Config._validate_positive_int(
                raw_dict, "points_per_ghost", 200
            ),
        )
