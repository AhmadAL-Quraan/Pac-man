from .player_score_storage import PlayerScoreStorage


class PlayerScore:
    scores: list[tuple[str, int]]
    storage: PlayerScoreStorage

    def add_score(self, name: str, score: int) -> None:
        """Add top 10 score to score file

        Args:
            name: Name of the file
            score: Score achieved
        """
        if self.is_valid_name(name) and self.is_valid_score(score):
            self.scores.append((name, score))
            self.scores.sort(key=lambda entry: entry[1], reverse=True)
            self.scores = self.scores[:10]
            self.storage.save(self.scores)
        else:
            print("Not valid name or score")

    def is_valid_name(self, name: str) -> bool:
        """Check validation of a name: max 10 characters, alphanumeric and
        spaces only.

        Args:
            name: The player's entered name.

        Returns:
            True if the name is valid, False otherwise.
        """
        if not name or len(name) > 10:
            return False
        return all(char.isalnum() or char == " " for char in name)

    def is_valid_score(self, score: int) -> bool:
        """Check validation of score: Non-negative"""
        if score >= 0:
            return True
        return False

    def show_top(self) -> list[tuple[str, int]]:
        """Show top 10 scores"""
        return self.storage.load()[:10]
