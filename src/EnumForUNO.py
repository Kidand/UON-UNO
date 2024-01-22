from enum import Enum


class DifficultyLevel(Enum):
    easy = "easy"
    normal = "normal"
    hard = "hard"


class Button(Enum):
    wild = "wild"
    checked = "checked"
    exchange = "exchange"
    next = "next"


class Color(Enum):
    blue = "blue"
    green = "green"
    red = "red"
    yellow = "yellow"
    other = "other"


class CardFunc(Enum):
    skip = "skip"
    reverse = "reverse"
    take_two = "take2+"
    take_four = "take4+"
    change_color = "change_color"
