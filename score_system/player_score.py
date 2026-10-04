from .player_score_storage import PlayerScoreStorage


class PlayerScore:
    scores: list[tuple[str, int]]
    storage: PlayerScoreStorage
    filepath: str

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.storage = PlayerScoreStorage()
        self.scores = self.storage.load(self.filepath)

    def add_score(self, name: str, score: int) -> None:
        """Add top 10 score to score file"""
        if self.is_valid_name(name) and self.is_valid_score(score):
            self.scores.append((name, score))
            self.scores.sort(key=lambda entry: entry[1], reverse=True)
            self.scores = self.scores[:10]
        else:
            print("Not valid name or score")

    def is_valid_name(self, name: str) -> bool:
        if not name or len(name) > 10:
            return False
        return all(char.isalnum() or char == " " for char in name)

    def is_valid_score(self, score: int) -> bool:
        return score >= 0

    def show_top(self) -> list[tuple[str, int]]:
        """Show top 10 scores"""
        return self.scores[:10]

    def save(self):
        self.storage.save(self.scores, self.filepath)

    def load(self, filepath: str):
        return self.storage.load(filepath)
