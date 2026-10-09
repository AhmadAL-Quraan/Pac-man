from dataclasses import dataclass


@dataclass
class PlayerScoreStorage:
    """Class representing PlayerScoreStorage."""

    def load(self, filepath: str) -> list[tuple[str, int]]:
        """Function representing load."""
        score: list[tuple[str, int]] = []
        try:
            with open(filepath, "r") as f:
                content = f.read().strip()

                if not content:
                    return score

                splitting = content.split("\n")

                for i in splitting:
                    if not i.strip():
                        continue

                    divide: list[str] = i.split(":")

                    if len(divide) >= 2:
                        score.append((divide[0], int(divide[1])))

        except (Exception, FileNotFoundError) as e:
            print(f"File error: {e}")

        return score

    def save(self, scores: list[tuple[str, int]], filepath: str) -> None:
        """Function representing save."""
        with open(filepath, "w") as f:
            for name, score in scores:
                f.write(f"{name}:{score}\n")
