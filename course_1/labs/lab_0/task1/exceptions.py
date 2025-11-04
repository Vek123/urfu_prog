__all__ = [
    "GameOver",
    "Win",
]


class GameOver(Exception):
    pass


class Win(Exception):
    pass


class NextLevel(Exception):
    pass
