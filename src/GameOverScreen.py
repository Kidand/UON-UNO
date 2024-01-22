import sys

import pygame

from src.UtilForUNO import Util

pygame.init()
screen = pygame.display.set_mode((1280, 800))
go_background1 = pygame.image.load("uno-cards/others/UoN_Card_Back.png").convert_alpha()
go_background_image = pygame.image.load("uno-cards/others/uon_trent_building.jpg").convert_alpha()
go_background2 = pygame.transform.scale(go_background_image, (1280, 800))


class ellipse_button:
    def __init__(self, x, y, colour, text, width, height, size, font_colour, intro):
        self.x = x
        self.y = y
        self.colour = colour
        self.text = text
        self.width = width
        self.height = height
        self.size = size
        self.font_colour = font_colour
        self.intro = intro

    def draw(self):
        pygame.font.init()
        my_font = pygame.font.SysFont("century ", self.size)
        text = my_font.render(self.text, True, self.font_colour)
        pygame.draw.ellipse(screen, self.colour, ((self.x - self.width // 2), (self.y - self.height // 2),
                                                  self.width, self.height))
        screen.blit(text, (int(self.x - text.get_width() // 2), int(self.y - text.get_height() // 2)))

    def mouse_position(self, drawn):
        position = pygame.mouse.get_pos()
        global position_value
        if (self.x - self.width / 2) < position[0] < (self.x + self.width / 2) and (self.y - self.height / 2) < \
                position[1] < (self.y + self.height / 2) and drawn == False:
            position_value = True
            drawn = True
            ring_colour = 'yellow'
            if self == play_again_icon:
                pygame.draw.rect(screen, pygame.Color(ring_colour), pygame.Rect(278, 606, 300, 82), 3, 10)
            if self == quit_icon:
                pygame.draw.rect(screen, pygame.Color(ring_colour), pygame.Rect(681, 606, 300, 82), 3, 10)
            pygame.display.flip()
            drawn = True
        else:
            position_value = False
            ring_colour = 'beige'
            pygame.draw.rect(screen, pygame.Color(ring_colour), pygame.Rect(278, 606, 300, 82), 3, 10)
            pygame.draw.rect(screen, pygame.Color(ring_colour), pygame.Rect(681, 606, 300, 82), 3, 10)
            pygame.display.flip()
            drawn = False

    def mouseclick(self):
        global game_over
        if position_value:
            if pygame.mouse.get_pressed()[0]:
                if self == quit_icon:
                    print("quit")
                    pygame.quit()
                    sys.exit()
                if self == play_again_icon:
                    menu = True
                    print("play again")
                    game_over = False
                    return menu


class Buttons:
    transparency = 0

    def __init__(self, x=None, y=None, colour=None, text=None, width_b=None, height=None, size=None, font_colour=None,
                 button_colour=None, button_function=None):
        self.x = x
        self.y = y
        self.colour = colour
        self.text = str(text)
        self.width = width_b
        self.height = height
        self.size = size
        self.font_colour = font_colour
        self.button_colour = button_colour
        self.button_function = button_function

    def draw(self):
        pygame.font.init()
        my_font = pygame.font.SysFont("century ", self.size)
        text = my_font.render(self.text, True, self.font_colour)
        pygame.draw.rect(screen, self.colour, ((self.x - self.width // 2), (self.y - self.height // 2),
                                               self.width, self.height))
        screen.blit(text, (int(self.x - text.get_width() // 2), int(self.y - text.get_height() // 2)))


class Game_over(Buttons, ellipse_button):
    def run_game_over(self, score_list):

        def get_score(player):
            name, score = player
            return score

        sorted_players = sorted(score_list, key=get_score, reverse=True)

        if sorted_players[-1][0] == 0:
            outcome = "You Win!"
            width = 800
        if sorted_players[-1][0] == 1:
            outcome = Util.get_player_name(1) + " Wins"
            width = 1100
        if sorted_players[-1][0] == 2:
            outcome = Util.get_player_name(2) + " Wins"
            width = 1000
        if sorted_players[-1][0] == 3:
            outcome = Util.get_player_name(3) + " Wins"
            width = 1200

        leaderboard = []
        for _ in range(len(sorted_players)):
            if sorted_players[_][0] == 0:
                leaderboard.append("You")
            if sorted_players[_][0] == 1:
                leaderboard.append(Util.get_player_name(1))
            if sorted_players[_][0] == 2:
                leaderboard.append(Util.get_player_name(2))
            if sorted_players[_][0] == 3:
                leaderboard.append(Util.get_player_name(3))

        win_or_lose_icon = ellipse_button(640, 400, (255, 0, 0), outcome, width, 280, 150, (255, 255, 0), False)

        self.go_animation(win_or_lose_icon, score_list, sorted_players, leaderboard)

        # pygame.display.flip()

        global game_over
        game_over = True
        menu = None
        drawn = False
        while game_over:
            ellipse_button.mouse_position(quit_icon, drawn)
            ellipse_button.mouseclick(quit_icon)
            ellipse_button.mouse_position(play_again_icon, drawn)
            menu = ellipse_button.mouseclick(play_again_icon)
            pygame.init()

            if not game_over:
                return menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    global quit_icon
    global play_again_icon

    play_again_icon = Buttons(430, 650, pygame.Color('beige'), "Play Again", 290, 70, 50, pygame.Color('azure4')
                              , False)
    quit_icon = Buttons(830, 650, pygame.Color('beige'), "Quit", 290, 70, 50, pygame.Color('azure4'), False)

    def go_animation(self, win_or_lose_icon, score_list, sorted_players, leaderboard):
        # screen.blit(go_background2, (0, 0))
        import time
        y = 0
        for i in range(0, 60):
            x = 0
            if x in range(0, 1200):
                if y in range(0, 800):
                    time.sleep(0.001)
                    screen.blit(go_background1, (x, y))
                    pygame.display.flip()

            for j in range(0, 50):
                x = x + 30
                y = y - 50
                if x in range(0, 1280):
                    if y in range(0, 900):
                        time.sleep(0.001)
                        screen.blit(go_background1, (x, y))
                        pygame.display.flip()

            y = 50 * i
            ellipse_button.draw(win_or_lose_icon)

        for i in range(0, 60):
            x = 0
            if x in range(0, 1200):
                if y in range(0, 800):
                    time.sleep(.001)
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 30, 50))
                    pygame.display.flip()

            for j in range(0, 50):
                x = x + 30
                y = y - 50
                if x in range(0, 1280):
                    if y in range(0, 800):
                        time.sleep(.001)
                        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 30, 50))
                        pygame.display.flip()
            y = 50 * i
        screen.fill((255, 255, 255))
        pygame.display.flip()
        transparency = 0
        for _ in range(0, 128):
            transparency = transparency + 1
            go_background2.set_alpha(transparency)
            screen.blit(go_background2, (0, 0))
            pygame.display.flip()
            time.sleep(0.005)

        leaderboard = leaderboard[::-1]
        if len(leaderboard) < 4:
            while len(leaderboard) < 4:
                leaderboard.append('-')
        leaderboard = leaderboard[::-1]

        sorted_players = sorted_players[::-1]
        if len(sorted_players) < 4:
            for i in range(4 - len(sorted_players)):
                sorted_players.append(("-", "-"))

        leaderboard_icon = Buttons(640, 300, pygame.Color('darkblue'), "", 750, 450, 40, pygame.Color('grey82'), False)

        pygame.draw.rect(screen, pygame.Color('grey82'), pygame.Rect(255, 65, 770, 470), 30, 23)
        pygame.draw.rect(screen, pygame.Color('darkblue'), pygame.Rect(260, 70, 760, 460), 17, 12)
        pygame.draw.rect(screen, pygame.Color('beige'), pygame.Rect(681, 608, 300, 80), 17, 12)
        pygame.draw.rect(screen, pygame.Color('beige'), pygame.Rect(278, 608, 300, 80), 17, 12)

        name_cell1 = ellipse_button(644.1, 145, pygame.Color('beige'), str(leaderboard[3]), 233.3, 75, 40,
                                    pygame.Color('azure4'), True)
        point_cell1 = ellipse_button(890, 145, pygame.Color('beige'), str(sorted_players[0][1]), 233.3, 75, 40,
                                     pygame.Color('azure4'), True)
        rank_cell1 = ellipse_button(398.3, 145, pygame.Color('beige'), "#1", 233.3, 75, 40, pygame.Color('azure4'),
                                    True)

        name_cell2 = ellipse_button(641.1, 245, pygame.Color('beige'), str(leaderboard[2]), 233.3, 75, 40,
                                    pygame.Color('azure4'), True)
        point_cell2 = ellipse_button(890, 245, pygame.Color('beige'), str(sorted_players[1][1]), 233.3, 75, 40,
                                     pygame.Color('azure4'),
                                     True)
        rank_cell2 = ellipse_button(398.3, 245, pygame.Color('beige'), "#2", 233.3, 75, 40, pygame.Color('azure4'),
                                    True)

        name_cell3 = ellipse_button(641.1, 345, pygame.Color('beige'), str(leaderboard[1]), 233.3, 75, 40,
                                    pygame.Color('azure4'), True)
        point_cell3 = ellipse_button(890, 345, pygame.Color('beige'), str(sorted_players[2][1]), 233.3, 75, 40,
                                     pygame.Color('azure4'),
                                     True)
        rank_cell3 = ellipse_button(398.3, 345, pygame.Color('beige'), "#3", 233.3, 75, 40, pygame.Color('azure4'),
                                    True)
        name_cell4 = ellipse_button(641.1, 445, pygame.Color('beige'), str(leaderboard[0]), 233.3, 75, 40,
                                    pygame.Color('azure4'), True)
        point_cell4 = ellipse_button(890, 445, pygame.Color('beige'), str(sorted_players[3][1]), 233.3, 75, 40,
                                     pygame.Color('azure4'), True)
        rank_cell4 = ellipse_button(398.3, 445, pygame.Color('beige'), "#4", 233.3, 75, 40, pygame.Color('azure4'),
                                    True)

        Buttons.draw(leaderboard_icon)
        ellipse_button.draw(name_cell1)
        ellipse_button.draw(name_cell2)
        ellipse_button.draw(name_cell3)
        ellipse_button.draw(name_cell4)
        ellipse_button.draw(point_cell1)
        ellipse_button.draw(point_cell2)
        ellipse_button.draw(point_cell3)
        ellipse_button.draw(point_cell4)
        ellipse_button.draw(rank_cell1)
        ellipse_button.draw(rank_cell2)
        ellipse_button.draw(rank_cell3)
        ellipse_button.draw(rank_cell4)
        Buttons.draw(play_again_icon)
        Buttons.draw(quit_icon)


if __name__ == "__main__":
    menu = Game_over.run_game_over(Game_over(), [(0, 24), (1, 37), (2, 50)])
