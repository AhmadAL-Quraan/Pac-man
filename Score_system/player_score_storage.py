from dataclasses import dataclass


@dataclass
class PlayerScoreStorage:
    filepath: str = "test.txt"

    def load(self) -> list[tuple[str, int]]:
        score: list[tuple[str, int]] = []
        try:
            with open(self.filepath, "r") as f:
                data_score: list[tuple[str, int]] = []
                name_extract: str = ""
                splitting = f.read().split()
                for i in splitting:
                    divide: list[str] = i.split(":")
                    score.append((divide[0], int(divide[1])))
        except (Exception, FileNotFoundError) as e:
            print(f"File error: {e}")

        return score

    def save(self, scores: list[tuple[str, int]]) -> None:
        with open(self.filepath, "a") as f:
            for name, score in scores:
                f.write(f"{name}:{score}")
                f.write("\n")
