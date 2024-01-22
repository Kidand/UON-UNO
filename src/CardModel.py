import copy
import uuid
from enum import Enum
from pathlib import Path

from src.EnumForUNO import CardFunc


class Card:

    def __init__(self, value: str, color: str):
        self.card_id = uuid.uuid4().hex
        self.value = value
        self.color = color
        self.image_addr = Path(f"uno-cards/{self.color}/{self.value}.png")
        self.image_back_addr = Path("uno-cards/others/UoN_Card_Back.png")
        self.x_location = None
        self.y_location = None
        self.card_score = None
        self.selected = False

    def __repr__(self):
        return self.value + self.card_id[:5]

    def get_color(self):
        return self.color

    def get_value(self):
        if self.color == "other":
            result = self.value.replace("X", "")
            return result
        else:
            result = self.value.replace(self.color, "")
            return result

    def get_image_addr(self):
        return self.image_addr

    def get_image_back_addr(self):
        return self.image_back_addr

    def get_func(self):
        return []

    def set_location(self, x, y):
        self.x_location = x
        self.y_location = y

    def get_score(self):
        return self.card_score

    def select(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True
        return self.selected

    def get_selected(self):
        return self.selected


class NumberCard(Card):
    def get_score(self):
        self.card_score = int(self.value[-1:]) + 1
        return self.card_score


class SkipCard(Card):
    def get_func(self):
        return [CardFunc.skip, ]

    def get_score(self):
        self.card_score = 20
        return self.card_score


class ReverseCard(Card):
    def get_func(self):
        return [CardFunc.reverse, ]

    def get_score(self):
        self.card_score = 20
        return self.card_score


class TakeTwoPlus(Card):
    def get_func(self):
        return [CardFunc.take_two, ]

    def get_score(self):
        self.card_score = 20
        return self.card_score


class WildCard(Card):
    def get_func(self):
        return [CardFunc.change_color, ]

    def change_color(self, diff_color):
        if isinstance(diff_color, Enum):
            diff_color = diff_color.value
        self.value = diff_color + "wild"
        self.color = diff_color
        self.image_addr = Path(f"uno-cards/{self.color}/{self.value}.png")

    def get_score(self):
        self.card_score = 50
        return self.card_score


class TakeFourPlus(WildCard):
    def get_func(self):
        result = copy.deepcopy(super().get_func())
        result.extend([CardFunc.take_four, ])

        return result

    def change_color(self, diff_color):
        if isinstance(diff_color, Enum):
            diff_color = diff_color.value
        self.value = self.value.replace("X", diff_color)
        self.color = diff_color
        self.image_addr = Path(f"uno-cards/{self.color}/{self.value}.png")
