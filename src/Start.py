from src import NumberOfPlayers
from src.Main import UnoMain
from src.MenuStates import MenuForUNO
from src.NumberOfPlayers import *
from src.GameOverScreen import *


running = True
menu = True
choose_player = False
uno_game = False
leaderboard = False
choose_player_result = None
score_list = []
while running:
    while menu:
        # menu page, rule page and Art design by Becky
        MenuForUNO.menufunc()
        menu = False
        choose_player = True

    while choose_player:
        # choose player and choose difficulty by Tom
        choose_player_result = UnoPlayerCount.run_num_players()
        NumberOfPlayers.state = False
        NumberOfPlayers.active = True
        choose_player = False
        uno_game = True

    while uno_game:
        #  The gameplay of the game and the logic of the robot by J.Yan, Tom and T.Chen
        score_list = UnoMain.run_game(choose_player_result)
        uno_game = False
        leaderboard = True

    while leaderboard:
        # leader board by Matt
        print(score_list)
        finale = Game_over()
        menu = Game_over.run_game_over(finale, score_list)
        leaderboard = False
        choose_player_result = None
        # Determine whether the game continues or the game exits




