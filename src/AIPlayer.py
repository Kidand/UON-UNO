import random

from src.CardModel import WildCard, TakeFourPlus
from src.EnumForUNO import DifficultyLevel
from src.UtilForUNO import Util


class AIPlayer:

    def __init__(self, current_turn, turn_list, reverse_state, card_total_list, discard_pile_list, draw_pile_list):
        self.current_turn = current_turn
        self.turn_list = turn_list
        self.reverse_state = reverse_state
        self.card_total_list = card_total_list
        self.discard_pile_list = discard_pile_list
        self.draw_pile_list = draw_pile_list
        self.card_on_the_table = discard_pile_list[-1]
        self.current_card_list = self.card_total_list[current_turn]
        self.card_list = sorted(self.current_card_list, key=lambda x: str(x))

    def set_card_total_list(self, card_total_list):
        self.card_total_list = card_total_list
        self.current_card_list = self.card_total_list[self.current_turn]
        self.card_list = sorted(self.current_card_list, key=lambda x: str(x))

    def make_decision(self, difficulty_level=DifficultyLevel.easy):
        # easy pattern
        if difficulty_level == DifficultyLevel.easy:
            return self.simple_version()
        elif difficulty_level == DifficultyLevel.normal:
            return self.normal_version()
        elif difficulty_level == DifficultyLevel.hard:
            return self.hard_version()

    # easy level
    def simple_version(self):
        if self.consider_color_and_value() is not None:
            return self.consider_color_and_value()

        for card in self.card_list:
            if isinstance(card, WildCard) and len(self.card_list) > 1:
                # flag = random.randint(1, 10)
                if isinstance(card, TakeFourPlus) and Util.get_next_turn(self.current_turn, self.turn_list,
                                                                         self.reverse_state) == 0:
                    continue
                else:
                    if self.get_frequent_color(self.current_turn) is not None:
                        card.change_color(self.get_frequent_color(0))
                        return card

    # normal level
    def normal_version(self):
        if self.consider_color_and_value() is not None:
            return self.consider_color_and_value()

        for card in self.card_list:
            if isinstance(card, WildCard) and len(self.card_list) > 1:
                if self.get_frequent_color(self.current_turn) is not None:
                    card.change_color(self.get_frequent_color(self.current_turn))
                    return card
        return None

    # hard level
    def hard_version(self):
        if len(self.card_total_list[Util.get_next_turn(self.current_turn, self.turn_list, self.reverse_state)]) \
                >= len(self.card_total_list[self.current_turn]):
            return self.normal_version()
        else:
            for card in self.card_list:
                if isinstance(card, WildCard) and len(self.card_list) > 1:
                    if self.get_frequent_color(self.current_turn) is not None:
                        card.change_color(self.get_frequent_color(self.current_turn))
                        return card
            if self.consider_color_and_value(DifficultyLevel.hard) is not None:
                return self.consider_color_and_value(DifficultyLevel.hard)

        return None

    # AI exchange card logic
    def exchange_card(self):
        if len(self.card_total_list[self.current_turn]) == 1 and self.consider_color_and_value() is not None:
            print("not exchange")
            message = " doesn't exchange a card and "
            resullt = [message, self.card_total_list, self.draw_pile_list, self.discard_pile_list]
            return resullt
        else:
            exchange_card = None
            if self.get_frequent_color(self.current_turn) is not None:
                for card_obj in self.current_card_list:
                    if card_obj.get_color() == self.get_frequent_color(self.current_turn):
                        exchange_card = card_obj
                if exchange_card is None:
                    exchange_card = random.choice(self.current_card_list)

            card_index = self.card_total_list[self.current_turn].index(exchange_card)
            self.card_total_list[self.current_turn][card_index] = self.draw_pile_list[0]
            print("AI: " + Util.get_player_name(self.current_turn) + " " + str(
                self.current_turn) + " decide exchange card: " + str(exchange_card))
            del (self.draw_pile_list[0])
            self.discard_pile_list.insert(0, exchange_card)
            message = " exchange a card and "
            result = [message, self.card_total_list, self.draw_pile_list, self.discard_pile_list]
            return result

    # consider color and value
    def consider_color_and_value(self, difficulty_level=None):
        if difficulty_level is not None:
            self.card_list = sorted(self.card_list, key=lambda x: str(x), reverse=True)

        for card in self.card_list:
            if card.get_color() == self.card_on_the_table.get_color():
                return card

        for card in self.card_list:
            if card.get_value() == self.card_on_the_table.get_value():
                return card

        return None

    # Gets the most frequent color in the card
    def get_frequent_color(self, turn_num):
        color_dict = {"blue": 0, "red": 0, "yellow": 0, "green": 0}
        for card_obj in self.card_total_list[turn_num]:
            if card_obj.get_color() != "others":
                color_dict[card_obj.get_color()] += 1
        result = sorted(color_dict.items(), key=lambda x: x[1])
        if len(result):
            return result[-1][0]
        else:
            return None
