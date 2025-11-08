__all__ = [
    "GameOver",
    "Win",
    "NextLevel",
]


class GameOver(Exception):
    pass


class Win(Exception):
    pass


class NextLevel(Exception):
    pass
