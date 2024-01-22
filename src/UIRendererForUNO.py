from pathlib import Path

import pygame

from src.EnumForUNO import *
from src.UtilForUNO import Util

pygame.init()

discard_state = True
uno_state = False


class DrawUi:
    # init pygame display info
    def __init__(self, player_num: int):
        self.player_num = player_num
        width, height = (1280, 800)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.flip()
        pygame.display.set_caption('UNO')

    def draw_background(self):
        imp_background = pygame.image.load(Path("uno-cards/background-image/background.png")).convert()
        self.screen.blit(imp_background, (0, 0))

    def draw_player_ui(self, state=None):
        if state == Button.exchange:
            checked_button = pygame.image.load(Path("uno-cards/button/exchange.png")).convert_alpha()
            self.screen.blit(checked_button, (900, 710))
        elif state == Button.checked:
            checked_button = pygame.image.load(Path("uno-cards/button/checked.png")).convert_alpha()
            self.screen.blit(checked_button, (970, 710))
        elif state == Button.wild:
            self.draw_wild_card()
        elif state == Button.next:
            checked_button = pygame.image.load(Path("uno-cards/button/next.png")).convert_alpha()
            self.screen.blit(checked_button, (1040, 710))
        else:
            pass

    # draw every player's cards by player number
    def draw_player_cards(self, card_total_list, current_turn, reverse_state):
        self.draw_player_name(current_turn)
        self.draw_deck(card_total_list[-1])
        self.draw_turn_arrow(reverse_state)
        for num in range(self.player_num - 1, -1, -1):
            color = (0, 0, 0)
            if num == 0:
                if num == current_turn:
                    color = (255, 255, 255)
                x_location = 425
                pygame.draw.rect(self.screen, color, pygame.Rect(420, 595, 440, 110), 4)
            elif num == 1:
                if num == current_turn:
                    color = (255, 255, 255)
                x_location = 785
                pygame.draw.rect(self.screen, color, pygame.Rect(420, 45, 440, 110), 4)
            elif num == 2:
                if num == current_turn:
                    color = (255, 255, 255)
                y_location = 530
                pygame.draw.rect(self.screen, color, pygame.Rect(1025, 165, 110, 440), 4)
            elif num == 3:
                if num == current_turn:
                    color = (255, 255, 255)
                y_location = 170
                pygame.draw.rect(self.screen, color, pygame.Rect(145, 165, 110, 440), 4)
            card_list = card_total_list[num]

            for card in card_list:
                if num == 0:
                    y_location = 600
                    image_addr = Util.get_card_image_addr(card)
                    card.set_location(x_location, y_location)
                    card_img = pygame.image.load(image_addr).convert()
                    if card.get_selected():
                        y_location -= 30
                    self.screen.blit(card_img, (x_location, y_location))
                    x_location += 40
                else:
                    image_addr = Util.get_card_image_back_addr(card)
                    card_img = pygame.image.load(image_addr).convert()
                    if num == 1:
                        y_location = 50
                        if card.get_selected():
                            y_location += 30
                        card_img_rotate = pygame.transform.rotate(card_img, 180)
                        card.set_location(x_location, y_location)
                        self.screen.blit(card_img_rotate, (x_location, y_location))
                        x_location -= 40
                    if num == 2:
                        x_location = 1030
                        if card.get_selected():
                            x_location -= 30
                        card_img_rotate = pygame.transform.rotate(card_img, 90)
                        card.set_location(x_location, y_location)
                        self.screen.blit(card_img_rotate, (x_location, y_location))
                        y_location -= 40
                    if num == 3:
                        x_location = 150
                        if card.get_selected():
                            x_location += 30
                        card_img_rotate = pygame.transform.rotate(card_img, 270)
                        card.set_location(x_location, y_location)
                        self.screen.blit(card_img_rotate, (x_location, y_location))
                        y_location += 40
            print(Util.get_player_name(num) + " " + str(num) + ": " + str(card_list))

    def draw_on_the_desk(self, discard_pile_list):
        if len(discard_pile_list):
            card_obj = discard_pile_list[-1]
            image_addr = Util.get_card_image_addr(card_obj)
            card_obj.set_location(470, 350)
            card_img = pygame.image.load(image_addr).convert()

            self.screen.blit(card_img, (card_obj.x_location, card_obj.y_location))  # 600 450
            print(str(card_obj) + " on the table")

    def draw_deck(self, draw_pile_list):
        color = (0, 0, 0)
        font = pygame.font.SysFont("Segoe UI", 20, True)
        draw_pile = font.render("Draw", True, color)
        discard_pile = font.render("Discard", True, color)
        self.screen.blit(draw_pile, (750, 320))
        self.screen.blit(discard_pile, (470, 320))
        if len(draw_pile_list):
            x_location = 740  # 900
            y_location = 350  # 400
            back_of_card = pygame.image.load(Util.get_card_image_back_addr(draw_pile_list[0])).convert()
            self.screen.blit(back_of_card, (x_location, y_location))

    def draw_turn_arrow(self, reverse_state):
        turn_arrow = pygame.image.load(Path("uno-cards/icon/turn_arrow.png")).convert_alpha()
        if reverse_state:
            turn_arrow = pygame.transform.flip(turn_arrow, False, True)
        self.screen.blit(turn_arrow, (420, 155))

    def draw_player_name(self, current_turn):
        font = pygame.font.Font(Path("fonts/Pacifico.ttf"), 30)
        for num in range(self.player_num):
            player_color = (0, 0, 0)
            if num == 0:
                if num == current_turn:
                    player_color = (255, 255, 255)
                player_name = font.render(Util.get_player_name(num), True, player_color)
                self.screen.blit(player_name, (420, 705))
            if num == 1:
                if num == current_turn:
                    player_color = (255, 255, 255)
                player_name = font.render(Util.get_player_name(num), True, player_color)
                self.screen.blit(player_name, (865, 45))
            if num == 2:
                if num == current_turn:
                    player_color = (255, 255, 255)
                player_name = font.render(Util.get_player_name(num), True, player_color)
                self.screen.blit(player_name, (1140, 550))
            if num == 3:
                if num == current_turn:
                    player_color = (255, 255, 255)
                player_name = font.render(Util.get_player_name(num), True, player_color)
                self.screen.blit(player_name, (20, 150))

    def draw_message(self, message):
        message_color = (0, 0, 0)
        font = pygame.font.SysFont("Segoe UI", 20, True)
        player_name = font.render(message, True, message_color)
        self.screen.blit(player_name, (20, 760))
        # self.screen.blit(player_name, (480, 260))

    def draw_score(self):
        score_color = (255, 255, 255)
        font = pygame.font.SysFont("Segoe UI", 24)
        score = font.render('Score', True, score_color)
        self.screen.blit(score, (20, 10))
        if self.player_num > 0:
            player1_score = font.render('Player1', True, score_color)
            self.screen.blit(player1_score, (20, 35))
        if self.player_num > 1:
            ai1_score = font.render('Ai1', True, score_color)
            self.screen.blit(ai1_score, (20, 60))
        if self.player_num > 2:
            ai2_score = font.render('Ai2', True, score_color)
            self.screen.blit(ai2_score, (20, 85))
        if self.player_num > 3:
            ai3_score = font.render('Ai3', True, score_color)
            self.screen.blit(ai3_score, (20, 110))

    def draw_discard_message(self):
        score_color = (255, 255, 255)
        font = pygame.font.SysFont("Segoe UI", 30)
        message_part1 = font.render('You are in discard state! You need', True, score_color)
        message_part2 = font.render('to remove one card from your hand ', True, score_color)
        message_part3 = font.render('and draw one from the pile!', True, score_color)
        self.screen.blit(message_part1, (1100, 850))
        self.screen.blit(message_part2, (1100, 875))
        self.screen.blit(message_part3, (1100, 900))

    def draw_wild_card(self):
        blue_button = pygame.image.load(Path("uno-cards/button/pickblue.png")).convert_alpha()
        green_button = pygame.image.load(Path("uno-cards/button/pickgreen.png")).convert_alpha()
        red_button = pygame.image.load(Path("uno-cards/button/pickred.png")).convert_alpha()
        yellow_button = pygame.image.load(Path("uno-cards/button/pickyellow.png")).convert_alpha()
        self.screen.blit(blue_button, (495, 490))
        self.screen.blit(green_button, (570, 490))
        self.screen.blit(red_button, (645, 490))
        self.screen.blit(yellow_button, (720, 490))

    def draw_uno_state(self, uno_state_list):
        for num, uno_state in uno_state_list:
            font = pygame.font.Font(Path("fonts/Pacifico.ttf"), 30)
            uno_color = (255, 255, 255)
            player_name = font.render("UNO!", True, uno_color)
            if num == 0 and uno_state:
                self.screen.blit(player_name, (520, 705))
            if num == 1 and uno_state:
                self.screen.blit(player_name, (990, 45))
            if num == 2 and uno_state:
                self.screen.blit(player_name, (1150, 600))
            if num == 3 and uno_state:
                self.screen.blit(player_name, (30, 200))
