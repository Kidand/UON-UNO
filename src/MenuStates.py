import sys

from pygame.locals import *

from MenuButtons import *

pygame.init()

screen_h = 800
screen_w = 1280
screen = pygame.display.set_mode((screen_w, screen_h))
background = pygame.image.load("uno-cards/others/uon_trent_building.jpg").convert_alpha()
background_img = pygame.transform.smoothscale(background, screen.get_size())
start_image = pygame.image.load("uno-cards/Buttons/START.png").convert_alpha()
rules_image = pygame.image.load("uno-cards/Buttons/RULES.png").convert_alpha()
exit_image = pygame.image.load("uno-cards/Buttons/EXIT.png").convert_alpha()
glow_image = pygame.image.load("uno-cards/Buttons/IMAGEGLOW.png").convert_alpha()
rulebook = pygame.image.load("uno-cards/others/RULESLIST.png").convert_alpha()
back_image = pygame.image.load("uno-cards/Buttons/BACK.png").convert_alpha()
rulebook_img = pygame.transform.scale(rulebook, (1200, 600))

BLACK = pygame.Color('black')

start_button = MenuButton(700, 250, start_image, 0.25, glow_image)
rules_button = MenuButton(700, 330, rules_image, 0.25, glow_image)
exit_button = MenuButton(700, 410, exit_image, 0.25, glow_image)
back_button = MenuButton(1020, 670, back_image, 0.25, glow_image)

class MenuForUNO:
    @classmethod
    def menufunc(cls):
        # game states
        menu_state = "main"
        cls.play_music()
        run = True
        while run:  # main game loop
            # screen.fill(WHITE) # in the event loop better
            menu_state = cls.get_menu(menu_state)
            pygame.display.update()
            if menu_state is None:
                run = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    @classmethod
    def get_menu(cls, menu_state):
        screen.blit(background_img, (0, 0))
        if menu_state == "main":
            # game title
            title_font = pygame.font.SysFont("century ", 100, True)
            title_color = (0, 0, 0)
            game_title = title_font.render("UNO", True, title_color)
            screen.blit(game_title, (50, 15))

            # main menu text
            font = pygame.font.SysFont("century ", 40)
            text_surface_obj = font.render('Main Menu', True, pygame.Color('grey82'), pygame.Color('darkblue'))
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (790, 200)
            screen.blit(text_surface_obj, text_rect_obj)
            if start_button.draw(screen):
                return None

            if rules_button.draw(screen):
                menu_state = "Rules"
                return menu_state

            if exit_button.draw(screen):
                pygame.quit()
                sys.exit()

        if menu_state == "Rules":
            screen.blit(background_img, (0, 0))
            screen.blit(rulebook_img, (20, 20))
            if back_button.draw(screen):
                menu_state = "main"
                return menu_state
        return menu_state

    @classmethod
    def play_music(cls):
        pygame.mixer.music.load("music/The_Nightingale.mp3")
        pygame.mixer.music.play(-1)  # continuous bg music
        pygame.mixer.music.set_volume(0.5)