import sys

import pygame

from src.EnumForUNO import DifficultyLevel
from src.MenuButtons import MenuButton

pygame.init()
width, height = (1280, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
pygame.display.set_caption('UNO')

running = True
base_font = pygame.font.SysFont("Segoe UI", 40)
user_text = ''
heading_font = pygame.font.SysFont("Pokemon GB.ttf", 40)
heading_color = (255, 255, 255)
# print(pygame.font.get_fonts())
uno_img = pygame.image.load("uno-cards/background-image/background_cut.png").convert()
uno_text = pygame.image.load("uno-cards/background-image/text2.png").convert()
active = False
header = heading_font.render('How many players do you want to play against 1, 2 or 3?', True, heading_color)
choose_diff = heading_font.render('Please choose a difficulty level or reset.', True, heading_color)

card2 = pygame.image.load("uno-cards/blue/blue2.png").convert()
card1 = pygame.image.load("uno-cards/blue/blue1.png").convert()
daniel = pygame.image.load("uno-cards/others/Daniel.png").convert_alpha()
transform_daniel = pygame.transform.scale(daniel, (100, 70))
colin = pygame.image.load("uno-cards/others/Colin.png").convert_alpha()
transform_colin = pygame.transform.scale(colin, (100, 70))
nottingham = pygame.image.load("uno-cards/others/University-of-Nottingham.png").convert_alpha()
transform_nottingham = pygame.transform.scale(nottingham, (200, 140))
num_players = [1, 2, 3]
clicking = False
i = 1
clock = pygame.time.Clock()
active = True
next_change_time = 0
num_of_players = None
state = False

class UnoPlayerCount:

    @classmethod
    def run_num_players(cls):
        global i, num_of_players
        global active
        global next_change_time
        global num_players
        global state

        # global num_of_players

        while running:
            time_now = pygame.time.get_ticks()
            screen.blit(uno_img, (0, 0))
            if active:
                screen.blit(header, (150, 200))
            else:
                screen.blit(choose_diff, (150, 200))

            card = pygame.image.load(f"uno-cards/blue/blue{num_players[i - 1]}.png").convert()
            transform_card = pygame.transform.scale(card, (70, 100))

            screen.blit(transform_card, (445, 435))
            if active:
                if (time_now > next_change_time):
                    if i == 3:
                        i = 1
                        next_change_time = time_now + 600
                    else:
                        i += 1
                        next_change_time = time_now + 600
            # event = None
            for event in pygame.event.get():
                # if user types QUIT then the screen will close
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    print(event.pos)

                    if x > 443 and x < 515 and y < 535 and y > 435:
                        print("clicked on image")
                        active = False
                        state = True
                        difficulty_choice = True
                        num_of_players = num_players[i - 1] + 1

            if state:
                easy = pygame.image.load("uno-cards/Buttons/EASY.png").convert_alpha()
                medium = pygame.image.load("uno-cards/Buttons/MEDIUM.png").convert_alpha()
                hard = pygame.image.load("uno-cards/Buttons/HARD.png").convert_alpha()
                reset = pygame.image.load("uno-cards/Buttons/RESET.png").convert_alpha()
                glow_image = pygame.image.load("uno-cards/Buttons/IMAGEGLOW.png").convert_alpha()
                easy_button = MenuButton(800, 275, easy, 0.25, glow_image)
                medium_button = MenuButton(800, 350, medium, 0.25, glow_image)
                hard_button = MenuButton(800, 425, hard, 0.25, glow_image)
                reset_button = MenuButton(800, 600, reset, 0.25, glow_image)

                if easy_button.draw(screen):
                    return [num_of_players, DifficultyLevel.easy]
                if medium_button.draw(screen):
                    return [num_of_players, DifficultyLevel.normal]
                if hard_button.draw(screen):
                    return [num_of_players, DifficultyLevel.hard]
                if reset_button.draw(screen):
                    active = True
                    state = False

            screen.blit(transform_card, (445, 435))
            clock.tick(30)

            pygame.display.update()
