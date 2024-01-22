import random

from src.CardModel import *


class Util:

    @classmethod
    def generate_card_list(cls):
        card_list = []
        # blue
        blue_list = [NumberCard(f"blue{num}", "blue") for num in range(10)]
        blue_list1 = [NumberCard(f"blue{num}", "blue") for num in range(1, 10)]
        blue_list2 = [SkipCard("blueSkip", "blue"), ReverseCard("blueRev", "blue"), TakeTwoPlus("bluePlus2", "blue"),
                      SkipCard("blueSkip", "blue"), ReverseCard("blueRev", "blue"), TakeTwoPlus("bluePlus2", "blue")]
        # green
        green_list = [NumberCard(f"green{num}", "green") for num in range(10)]
        green_list1 = [NumberCard(f"green{num}", "green") for num in range(1, 10)]
        green_list2 = [SkipCard("greenSkip", "green"), ReverseCard("greenRev", "green"),
                       TakeTwoPlus("greenPlus2", "green"),
                       SkipCard("greenSkip", "green"), ReverseCard("greenRev", "green"),
                       TakeTwoPlus("greenPlus2", "green")]

        # red
        red_list = [NumberCard(f"red{num}", "red") for num in range(10)]
        red_list1 = [NumberCard(f"red{num}", "red") for num in range(1, 10)]
        red_list2 = [SkipCard("redSkip", "red"), ReverseCard("redRev", "red"), TakeTwoPlus("redPlus2", "red"),
                     SkipCard("redSkip", "red"), ReverseCard("redRev", "red"), TakeTwoPlus("redPlus2", "red")]

        # yellow
        yellow_list = [NumberCard(f"yellow{num}", "yellow") for num in range(10)]
        yellow_list1 = [NumberCard(f"yellow{num}", "yellow") for num in range(1, 10)]
        yellow_list2 = [SkipCard("yellowSkip", "yellow"), ReverseCard("yellowRev", "yellow"),
                        TakeTwoPlus("yellowPlus2", "yellow"),
                        SkipCard("yellowSkip", "yellow"), ReverseCard("yellowRev", "yellow"),
                        TakeTwoPlus("yellowPlus2", "yellow")]

        # other
        other_card_list = [WildCard("Xwild", "others"), TakeFourPlus("X+4", "others"),
                           WildCard("Xwild", "others"), TakeFourPlus("X+4", "others"),
                           WildCard("Xwild", "others"), TakeFourPlus("X+4", "others"),
                           WildCard("Xwild", "others"), TakeFourPlus("X+4", "others")]

        card_list.extend(blue_list)
        card_list.extend(blue_list1)
        card_list.extend(blue_list2)
        card_list.extend(green_list)
        card_list.extend(green_list1)
        card_list.extend(green_list2)
        card_list.extend(red_list)
        card_list.extend(red_list1)
        card_list.extend(red_list2)
        card_list.extend(yellow_list)
        card_list.extend(yellow_list1)
        card_list.extend(yellow_list2)
        card_list.extend(other_card_list)
        return card_list

    @classmethod
    def card_distribution(cls, people_mum, init_card_num, card_list=None):
        if card_list is None:
            card_list = cls.generate_card_list()

        if card_list is not None:
            result_list = []
            for _ in range(people_mum):
                init_card_list = []
                for _ in range(init_card_num):
                    # random.seed(random.randint(1, 100))
                    choose_card = random.choice(card_list)
                    init_card_list.append(choose_card)
                    card_list.remove(choose_card)
                    if len(card_list) == 0:
                        result_list.append([])
                        return result_list
                result_list.append(init_card_list)
            # The remaining cards are stored as a list, result_list[-1], use random.shuffle
            random.shuffle(card_list)
            result_list.append(card_list)
            return result_list

    @classmethod
    def get_card_image_addr(cls, card_obj):
        return card_obj.get_image_addr()

    @classmethod
    def get_card_image_back_addr(cls, card_obj):
        return card_obj.get_image_back_addr()

    @classmethod
    def select_card(cls, card_obj, card_list):
        for card in card_list:
            if card_obj is card:
                card_obj.select()
            elif card.get_selected():
                card.select()
        return card_list

    @classmethod
    def select_cards(cls, card_obj_list, card_list):
        # make card list unselected
        for card in card_list:
            if card.get_selected():
                card.select()
        for card in card_list:
            for card_obj in card_obj_list:
                if card_obj is card:
                    card_obj.select()
        return card_list

    @classmethod
    def cancle_select(cls, card_list):
        for card in card_list:
            if card.get_selected():
                card.select()
        return card_list

    @classmethod
    def click_wild_card(cls, card_obj):
        return isinstance(card_obj, WildCard) and card_obj.get_selected()

    @classmethod
    def get_selected_card(cls, card_list):
        for card in card_list:
            if card.get_selected():
                return card

    @classmethod
    def get_selected_wild_card(cls, card_list):
        for card in card_list:
            if card.get_selected() and cls.click_wild_card(card):
                return card

    @classmethod
    def generate_turn_list(cls, player_number):
        if player_number == 2:
            turn_list = [0, 1]
        else:
            turn_list = [0, 2, 1, 3][:player_number]
        return turn_list

    @classmethod
    def get_next_turn(cls, turn_num, turn_list: list, reverse_state):
        if reverse_state:
            result = turn_list[(turn_list.index(turn_num) - 1) % len(turn_list)]
        else:
            result = turn_list[(turn_list.index(turn_num) + 1) % len(turn_list)]
        return result

    @classmethod
    def get_last_turn(cls, turn_num, turn_list: list, reverse_state):
        if reverse_state:
            result = turn_list[(turn_list.index(turn_num) + 1) % len(turn_list)]
        else:
            result = turn_list[(turn_list.index(turn_num) - 1) % len(turn_list)]
        return result

    @classmethod
    def draw_cards(cls, draw_cards_num, player_list, draw_pile_list, discard_pile_list):
        if len(draw_pile_list) < 5:
            draw_pile_list.extend(discard_pile_list[:-1])
            discard_pile_list = discard_pile_list[-1:]
        if len(draw_pile_list):
            current_draw_card = draw_pile_list[:draw_cards_num]
            print(current_draw_card)
            print("draw pile size: " + str(len(draw_pile_list)))
            player_list.extend(current_draw_card)
            player_list = cls.select_cards(current_draw_card, player_list)
            result = [player_list, draw_pile_list[draw_cards_num:], discard_pile_list]
            return result

    @classmethod
    def card_check(cls, card_on_the_table, selected_card, card_list):
        if len(card_list) < 2 and isinstance(selected_card, WildCard):
            return False
        result = card_on_the_table.get_color() == selected_card.get_color() \
                 or card_on_the_table.get_value() == selected_card.get_value()
        return result

    @classmethod
    def get_player_name(cls, player_num):
        if player_num == 0:
            return "Player"
        elif player_num == 1:
            return "Michael"
        elif player_num == 2:
            return "Trevor"
        elif player_num == 3:
            return "Franklin"
        else:
            return "Unknow"

    @classmethod
    def check_winner(cls, card_total_list):
        for card_list in card_total_list[:-1]:
            if len(card_list) == 0:
                player_num = card_total_list.index(card_list)
                return player_num
        return None

    @classmethod
    def count_score(cls, card_total_list):
        result_list = []
        for card_list in card_total_list[:-1]:
            score = 0
            for card_obj in card_list:
                score += card_obj.get_score()
            player_num = card_total_list.index(card_list)
            player_score = (player_num, score)
            result_list.append(player_score)
            result = sorted(result_list, key=lambda x: x[1])
        return result

    @classmethod
    def generate_uno_dict(cls, player_number):
        uno_dict = {}
        for i in range(player_number):
            uno_dict[i] = False
        return uno_dict

    @classmethod
    def check_uno_state(cls, card_list):
        if len(card_list) == 1:
            return True
        else:
            return False
