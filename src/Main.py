from pygame import QUIT

from src.AIPlayer import AIPlayer
from src.UIRendererForUNO import *
from MenuButtons import *
import sys


class UnoMain:
    @classmethod
    def run_game(cls, choose_player_result):
        # init player num
        player_number = choose_player_result[0]
        # init difficult level
        difficulty_level = choose_player_result[1]

        # init ai turn list
        turn_list = Util.generate_turn_list(player_number)
        current_turn = turn_list[0]

        # init 3 list: 4 player card list, draw pile, discard pile
        card_total_list = Util.card_distribution(player_number, 7)
        draw_pile_list = card_total_list[-1]
        discard_pile_list = []
        pause_list = []

        # UNO state dict
        # uno_dict = {0: True, 1: True, 2: True, 3: True}
        uno_dict = Util.generate_uno_dict(player_number)

        # switch
        reverse_state = False
        running = True
        wild_flag = False
        checked = False
        next_turn = False
        exchange = True
        draw_card = False

        # init user interface
        uno_ui = DrawUi(player_number)
        uno_ui.draw_background()
        uno_ui.draw_player_cards(card_total_list, current_turn, reverse_state)
        uno_ui.draw_player_ui()
        uno_ui.draw_uno_state(uno_dict.items())
        uno_ui.draw_discard_message()

        # usefulcard
        current_card = None

        # pause screen
        # game_paused = False
        # screen = pygame.display.set_mode((1280, 800))
        # background = pygame.image.load("uno-cards/others/uon_trent_building.jpg").convert_alpha()
        # background_img = pygame.transform.smoothscale(background, screen.get_size())
        # resume_image = pygame.image.load("uno-cards/Buttons/Resume.png").convert_alpha()
        # glow_image = pygame.image.load("uno-cards/Buttons/IMAGEGLOW.png").convert_alpha()
        # exit_image = pygame.image.load("uno-cards/Buttons/EXIT.png").convert_alpha()
        # resume_button = MenuButton(590, 300, resume_image, 0.25, glow_image)
        # paused_exit_button = MenuButton(590, 375, exit_image, 0.25, glow_image)

        # draw pic
        uno_ui.draw_background()
        uno_ui.draw_on_the_desk(discard_pile_list)
        uno_ui.draw_player_cards(card_total_list, current_turn, reverse_state)
        uno_ui.draw_uno_state(uno_dict.items())
        # main loop
        while running:
            # AI turn
            if current_turn != 0:
                message_str = ""
                turn_num = current_turn
                print("AI: " + Util.get_player_name(current_turn) + " " + str(
                    current_turn) + " TURN--------------------------------------------------")
                # make sure card unseleted
                card_total_list[turn_num] = Util.cancle_select(card_total_list[turn_num])

                # let AI make a decision
                ai = AIPlayer(current_turn, turn_list, reverse_state, card_total_list, discard_pile_list,
                              draw_pile_list)
                exchange_result = ai.exchange_card()
                ai.set_card_total_list(exchange_result[1])
                message_str += exchange_result[0]
                card_total_list = exchange_result[1]
                draw_pile_list = exchange_result[2]
                discard_pile_list = exchange_result[3]

                card_obj = ai.make_decision(difficulty_level)
                if card_obj is not None:
                    print("AI: " + Util.get_player_name(current_turn) + " " + str(
                        current_turn) + " choose to play " + str(card_obj))
                    discard_pile_list.append(card_obj)
                    card_total_list[current_turn].remove(card_obj)
                    func_str = ""
                    # check func_list
                    if len(card_obj.get_func()):
                        for f in card_obj.get_func():
                            if f == CardFunc.skip:
                                print("skip---------------------------")
                                current_turn = Util.get_next_turn(current_turn, turn_list, reverse_state)
                                func_str += Util.get_player_name(current_turn) + " is skipped."
                            if f == CardFunc.reverse:
                                print("reverse------------------------------------")
                                if reverse_state:
                                    reverse_state = False
                                else:
                                    reverse_state = True
                                func_str += "The turn is reversed!"
                            if f == CardFunc.take_two:
                                print("sKip and take two cards------------------------------")
                                current_turn = Util.get_next_turn(current_turn, turn_list, reverse_state)
                                result_list = Util.draw_cards(2, card_total_list[current_turn],
                                                              draw_pile_list,
                                                              discard_pile_list)
                                card_total_list[current_turn] = result_list[0]
                                draw_pile_list = result_list[1]
                                discard_pile_list = result_list[2]
                                func_str += Util.get_player_name(
                                    current_turn) + " is skipped and draw two cards."
                            if f == CardFunc.take_four:
                                print("sKip and take four cards------------------------------")
                                current_turn = Util.get_next_turn(current_turn, turn_list, reverse_state)
                                result_list = Util.draw_cards(4, card_total_list[current_turn], draw_pile_list,
                                                              discard_pile_list)
                                card_total_list[current_turn] = result_list[0]
                                draw_pile_list = result_list[1]
                                discard_pile_list = result_list[2]
                                func_str += Util.get_player_name(
                                    current_turn) + " is skipped and draw four cards."

                    message_str += "play " + card_obj.get_color() + " " + card_obj.get_value() + ". " + func_str
                else:
                    message_str += "draw a card."
                    result_list = Util.draw_cards(1, card_total_list[current_turn], draw_pile_list, discard_pile_list)
                    card_total_list[current_turn] = result_list[0]
                    draw_pile_list = result_list[1]
                    discard_pile_list = result_list[2]

                # next turn
                exchange = True
                checked = False
                current_turn = Util.get_next_turn(current_turn, turn_list, reverse_state)

                # check UNO state
                uno_dict[turn_num] = Util.check_uno_state(card_total_list[turn_num])

                # draw pic
                uno_ui.draw_background()
                uno_ui.draw_on_the_desk(discard_pile_list)
                uno_ui.draw_player_cards(card_total_list, current_turn, reverse_state)
                uno_ui.draw_message(Util.get_player_name(turn_num) + message_str)
                uno_ui.draw_uno_state(uno_dict.items())

                pygame.time.wait(2500)

            # 0 means player's turn
            if current_turn == 0:
                player_message = ""
                # add new rule: when player have only one card, he can choose to exchange or not
                if len(card_total_list[current_turn]) == 1:
                    checked = True
                    # draw_card = True

                # draw player ui
                if wild_flag:
                    uno_ui.draw_player_ui(Button.wild)
                if checked:
                    uno_ui.draw_player_ui(Button.checked)
                if exchange:
                    uno_ui.draw_player_ui(Button.exchange)
                if next_turn:
                    uno_ui.draw_player_ui(Button.next)

                # pause
                # if game_paused:
                #     screen.blit(background_img, (0, 0))
                #     pygame.display.set_caption('Pause Menu')
                #     if resume_button.draw(screen):
                #         game_paused = False
                #
                #     if paused_exit_button.draw(screen):
                #         pygame.quit()
                #         sys.exit()

                # event trigger
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # running = False
                        pygame.quit()
                        sys.exit()
                    # elif event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_SPACE:
                    #         game_paused = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        print('In the event loop:', event.pos, event.button)
                        print("Player TURN--------------------------------------------------")
                        # ----------------------------------------------------------------------
                        if wild_flag:
                            card_obj = Util.get_selected_wild_card(card_total_list[0])
                            if card_obj is not None:
                                if 495 < event.pos[0] < 560 and 490 < event.pos[1] < 555:
                                    card_obj.change_color(Color.blue)
                                elif 570 < event.pos[0] < 635 and 490 < event.pos[1] < 555:
                                    card_obj.change_color(Color.green)
                                elif 645 < event.pos[0] < 710 and 490 < event.pos[1] < 555:
                                    card_obj.change_color(Color.red)
                                elif 720 < event.pos[0] < 785 and 490 < event.pos[1] < 555:
                                    card_obj.change_color(Color.yellow)
                                else:
                                    break
                                if card_obj.get_selected() and card_obj.get_color() != Color.other:
                                    # check func_list
                                    func_str = ""
                                    if len(card_obj.get_func()):
                                        for f in card_obj.get_func():
                                            if f == CardFunc.take_four:
                                                print("sKip and take four cards------------------------------")
                                                current_turn = Util.get_next_turn(current_turn, turn_list,
                                                                                  reverse_state)
                                                result_list = Util.draw_cards(4, card_total_list[current_turn],
                                                                              draw_pile_list,
                                                                              discard_pile_list)
                                                card_total_list[current_turn] = result_list[0]
                                                draw_pile_list = result_list[1]
                                                discard_pile_list = result_list[2]
                                                func_str += Util.get_player_name(
                                                    current_turn) + " is skipped and draw four cards"
                                                if Util.get_next_turn(current_turn, turn_list, reverse_state) == 0:
                                                    exchange = True
                                    discard_pile_list.append(card_obj)
                                    card_total_list[0].remove(card_obj)
                                    player_message += "Player play " + card_obj.get_color() + " " + card_obj.get_value() + ". " + func_str
                                    current_card = None
                                    wild_flag = False
                                    checked = False
                                    next_turn = False
                                    # next turn
                                    current_turn = Util.get_next_turn(current_turn, turn_list, reverse_state)

                        # only player can click card
                        for card_obj in card_total_list[0]:
                            card_img = pygame.image.load(card_obj.image_addr).convert()

                            xl = card_obj.x_location
                            xr = xl + card_img.get_width()
                            if card_obj is not card_total_list[0][-1]:
                                xr -= 30

                            yd = card_obj.y_location
                            if card_obj.get_selected():
                                yd -= 30
                            yu = yd + card_img.get_height()

                            if xl < event.pos[0] < xr and yd < event.pos[1] < yu:
                                print(str(card_obj) + " score: " + str(card_obj.get_score()))
                                Util.select_card(card_obj, card_total_list[0])
                                current_card = card_obj
                                # click checked button
                        if next_turn:
                            if 1040 < event.pos[0] < 1104 and 710 < event.pos[1] < 774:
                                current_turn = Util.get_next_turn(current_turn, turn_list,
                                                                  reverse_state)
                                card_total_list[0] = Util.cancle_select(card_total_list[0])
                                current_card = None
                                next_turn = False
                        if checked:
                            if 970 < event.pos[0] < 1034 and 710 < event.pos[1] < 774:
                                card_obj = current_card
                                if Util.click_wild_card(card_obj):
                                    wild_flag = True
                                    checked = False
                                elif card_obj is not None and card_obj.get_selected():
                                    # check selected card can use or not
                                    if Util.card_check(discard_pile_list[-1], card_obj, card_total_list[current_turn]):
                                        discard_pile_list.append(card_obj)
                                        card_total_list[current_turn].remove(card_obj)
                                        current_card = None
                                        func_str = ""
                                        # check func_list
                                        if len(card_obj.get_func()):
                                            for f in card_obj.get_func():
                                                if f == CardFunc.skip:
                                                    print("skip---------------------------")
                                                    current_turn = Util.get_next_turn(current_turn, turn_list,
                                                                                      reverse_state)
                                                    func_str += Util.get_player_name(current_turn) + " is skipped."
                                                    if Util.get_next_turn(current_turn, turn_list, reverse_state) == 0:
                                                        exchange = True
                                                if f == CardFunc.reverse:
                                                    print("reverse------------------------------------")
                                                    if reverse_state:
                                                        reverse_state = False
                                                    else:
                                                        reverse_state = True
                                                    func_str += "The turn is reversed!"
                                                if f == CardFunc.take_two:
                                                    current_turn = Util.get_next_turn(current_turn, turn_list,
                                                                                      reverse_state)
                                                    print(
                                                        str(current_turn) + "sKip and take two cards------------------------------")
                                                    result_list = Util.draw_cards(2, card_total_list[current_turn],
                                                                                  draw_pile_list,
                                                                                  discard_pile_list)
                                                    card_total_list[current_turn] = result_list[0]
                                                    draw_pile_list = result_list[1]
                                                    discard_pile_list = result_list[2]
                                                    func_str += Util.get_player_name(
                                                        current_turn) + " is skipped and draw two cards."
                                                    if Util.get_next_turn(current_turn, turn_list, reverse_state) == 0:
                                                        exchange = True

                                        player_message += "Player play " + card_obj.get_color() + " " + card_obj.get_value() + ". " + func_str
                                        # next turn
                                        current_turn = Util.get_next_turn(current_turn, turn_list, reverse_state)
                                        checked = False
                                        next_turn = False
                                    else:
                                        print(str(card_obj) + " not match " + str(discard_pile_list[-1]))

                        # ----------------------------------------------------------------------

                        # make player draw a card
                        # if (not exchange and draw_card) \
                        #         or (exchange and draw_card and len(card_total_list[current_turn]) == 1):
                        if not exchange and draw_card:
                            if draw_card:
                                if 740 < event.pos[0] < 810 and 350 < event.pos[1] < 450:
                                    if len(draw_pile_list):
                                        # if len(card_total_list[current_turn]) == 1:
                                        #     exchange = False
                                        result_list = Util.draw_cards(1, card_total_list[current_turn], draw_pile_list,
                                                                      discard_pile_list)
                                        card_total_list[current_turn] = result_list[0]
                                        draw_pile_list = result_list[1]
                                        discard_pile_list = result_list[2]
                                        current_card = card_total_list[current_turn][-1]
                                        player_message += "Player draw a card."
                                        draw_card = False
                                        checked = True
                                        next_turn = True
                        else:
                            print("please select a card to exchange!")

                        # exchange a card
                        if exchange:
                            if 900 < event.pos[0] < 964 and 710 < event.pos[1] < 774:
                                if current_card is not None:
                                    if not len(discard_pile_list) and Util.click_wild_card(current_card):
                                        print("wild card can not exchange at first!")
                                        break
                                    card_obj = current_card
                                    print(str(card_obj) + " exchange to " + str(draw_pile_list[0]))
                                    card_index = card_total_list[0].index(card_obj)
                                    card_total_list[0][card_index] = draw_pile_list[0]
                                    exchange_card = card_total_list[0][card_index]
                                    Util.select_card(exchange_card, card_total_list[0])
                                    del (draw_pile_list[0])
                                    discard_pile_list.insert(0, card_obj)
                                    current_card = exchange_card
                                    player_message = "Player exchange a card."
                                    exchange = False
                                    checked = True
                                    draw_card = True
                        # ----------------------------------------------------------------------

                        # check UNO state
                        uno_dict[0] = Util.check_uno_state(card_total_list[0])

                        # draw pic
                        uno_ui.draw_background()
                        uno_ui.draw_on_the_desk(discard_pile_list)
                        uno_ui.draw_player_cards(card_total_list, current_turn, reverse_state)
                        uno_ui.draw_player_ui()
                        uno_ui.draw_uno_state(uno_dict.items())
                        uno_ui.draw_message(player_message)

            if Util.check_winner(card_total_list) is not None:
                print("winner is " + Util.get_player_name(Util.check_winner(card_total_list)))
                print(Util.count_score(card_total_list))

                running = False
                pass

            pygame.display.update()

        result = Util.count_score(card_total_list)

        return result


if __name__ == "__main__":
    UnoMain.run_game([4, DifficultyLevel.easy])
