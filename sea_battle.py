from random import randint
from copy import deepcopy
from time import sleep


class SeaBattle:

    limited_shots_mode = False

    class Player:

        def __init__(self, battle_field, user_field, amount_of_ships):
            self.name = input("   Enter your name: ")
            self.battle_field = battle_field
            self.user_field = user_field
            self.ships = amount_of_ships

    # --------------------------------------------------------------
    # ------------------------- Setters ----------------------------
    # --------------------------------------------------------------

    def _user_input_handler(self, lower_bound, higher_bound, message=""):
        process_commands = {"Q": self._quit, "H": self._help}
        while True:
            uinput = input("    Enter{}: ".format(message)).upper()
            print()
            try:
                if uinput in process_commands:
                    process_commands[uinput]()
                    continue
                if lower_bound <= int(uinput) <= higher_bound:
                    break
                raise ValueError
            except ValueError:
                print("You can write only numbers from: {}, to: {}".format(lower_bound, higher_bound))
                print()
        return int(uinput)

    def _set_field_params(self):
        min_size = 2
        max_size = 10
        print("Possible values for field size.")
        print("    Min size: {0} x {0}".format(min_size))
        print("    Max size: {0} x {0}".format(max_size))
        print()
        horizontal = self._user_input_handler(min_size, max_size, " value for horizontal")
        vertical = self._user_input_handler(min_size, max_size, " value for vertical")
        print("\n" * 10)
        return horizontal, vertical

    def _set_ship_amount(self, amount_of_tiles):
        max_ship_amount = int(amount_of_tiles * 0.3)
        print("Write amount of the ships decks.")
        print("There can be no less than 1, and no more than {}!".format(max_ship_amount))
        print()
        ships_amount = self._user_input_handler(1, max_ship_amount, " ships quantity")
        print("\n" * 10)
        return ships_amount

    def _set_shots(self, ships_amount, amount_of_tiles):
        print("Amount of shots can`t be less than ships amount: {}, and bigger than tiles amount: {}!"
              .format(ships_amount, amount_of_tiles))
        shots = self._user_input_handler(ships_amount, amount_of_tiles, " shots amount")
        print("\n" * 10)
        return shots

    # --------------------------------------------------------------
    # ---------------------- Game builders -------------------------
    # --------------------------------------------------------------

    def _generate_empty_field(self, horizontal, vertical):
        return [["0" for _ in range(horizontal)]for _ in range(vertical)]

    def _add_ships_on_field(self, ships, field):
        not_allowed_coordinates = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        while ships:
            continue_ = False
            hor, ver, = randint(0, len(field) - 1), randint(0, len(field[0]) - 1)
            if ships == 0:
                break
            if field[ver][hor] == "1":
                continue
            for x, y in not_allowed_coordinates:
                try:
                    if field[ver + x][hor + y] == "1":
                        continue_ = True
                        break
                except IndexError:
                    pass
            if continue_:
                continue
            ships -= 1
            field[ver][hor] = "1"
        return field

    def _limited_shots_mode_trigger(self):
        self.limited_shots_mode = True
        self._build_solo_game()

    def _build_solo_game(self):
        horizontal, vertical = self._set_field_params()
        ships_amount = self._set_ship_amount(horizontal * vertical)
        user_field = self._generate_empty_field(horizontal, vertical)
        battle_field = self._add_ships_on_field(ships_amount, deepcopy(user_field))
        shots = None
        if self.limited_shots_mode:
            shots = self._set_shots(ships_amount, horizontal * vertical)
        self._run_solo_game(battle_field, user_field, ships_amount, shots)

    def _build_versus_game(self):
        horizontal, vertical = self._set_field_params()
        ships_amount = self._set_ship_amount(horizontal * vertical)
        user_field_1 = self._generate_empty_field(horizontal, vertical)
        battle_field_1 = self._add_ships_on_field(ships_amount, deepcopy(user_field_1))
        user_field_2 = deepcopy(user_field_1)
        battle_field_2 = self._add_ships_on_field(ships_amount, deepcopy(user_field_2))
        print("Player 1")
        p_1 = self.Player(battle_field_1, user_field_1, ships_amount)
        print("Player 2")
        p_2 = self.Player(battle_field_2, user_field_2, ships_amount)
        print("\n" * 3)
        self._run_versus_game(p_1, p_2)

    # --------------------------------------------------------------
    # ----------------------- Game process -------------------------
    # --------------------------------------------------------------

    def _print_game_field(self, user_field, shots):
        print()
        if shots:
            print("Shots: {}".format(shots))
        print([str(x) for x in range(len(user_field[0]) + 1)])
        for i, line in enumerate(user_field, start=1):
            print(list(str(i)), line, sep="")
        print()

    def _get_shoot(self, max_hor_value, max_ver_value):
        print("Shot to:")
        hor = self._user_input_handler(1, max_hor_value, " horizontal") - 1
        ver = self._user_input_handler(1, max_ver_value, " vertical") - 1
        return hor, ver

    def _handle_shoot(self, hor, ver, battle_field, user_field):
        if battle_field[ver][hor] == "0":
            user_field[ver][hor] = "~"
        else:
            if user_field[ver][hor] != "X":
                user_field[ver][hor] = "X"
                return True
        return False

    def _max_shoot_values(self, field):
        hor = len(field[0])
        ver = len(field)
        return hor, ver

    def _run_solo_game(self, battle_field, user_field, ships_amount, shots):
        max_hor_value, max_ver_value = self._max_shoot_values(user_field)
        if shots is None:
            shots = "Unlimited"
        print("Type 'h' for help, or 'q' for quit")
        print("\n" * 3)
        while ships_amount and shots:
            self._print_game_field(user_field, shots)
            hor, ver = self._get_shoot(max_hor_value, max_ver_value)
            if self._handle_shoot(hor, ver, battle_field, user_field):
                ships_amount -= 1
            if isinstance(shots, int):
                shots -= 1
        print("\n" * 10)
        if not ships_amount:
            print("    Win! You have destroyed last ship!")
        else:
            print("    Sorry, you lose! You have no more shots!")
        sleep(3)
        print("\n" * 10)

    def _run_versus_game(self, player_1, player_2):
        max_hor_value, max_ver_value = self._max_shoot_values(player_1.user_field)
        print("Type 'h' for help, or 'q' for quit")
        print("\n" * 3)
        while player_1.ships and player_2.ships:
            for player in (player_1, player_2):
                if not player_1.ships or not player_2.ships:
                    break
                print("{}'s turn.".format(player.name))
                self._print_game_field(player.user_field, None)
                while self._handle_shoot(*self._get_shoot(max_hor_value, max_ver_value),
                                         player.battle_field, player.user_field):
                    print("        Got!")
                    print()
                    player.ships -= 1
                    if player.ships == 0:
                        print("{} Winner!!!".format(player.name))
                        break
                    print("    Shoot one more time!")
                    self._print_game_field(player.user_field, None)
                print("        Miss!")
                print()
        del player_1, player_2
        sleep(3)
        print("\n" * 10)

    # --------------------------------------------------------------
    # -------------------------- Menus -----------------------------
    # --------------------------------------------------------------

    def _help(self):
        print()
        print("    ~ - Tile of water")
        print("    0 - Fog")
        print("    X - Destroyed ship")
        print()

    def _quit(self):
        print("Are you sure you want to quit?")
        print()
        print("     Type 'yes' or press enter to proceed")
        answer = input("    Enter: ").upper()
        if answer == "YES" or answer == "Y":
            raise SystemExit

    def main_menu(self):
        self.limited_shots_mode = False
        menu_triggers = {"Q": self._quit, "S": self._build_solo_game, "V": self._build_versus_game,
                         "L": self._limited_shots_mode_trigger}
        while True:
            print("        Welcome to sea battle!")
            print()
            print("Type: For:")
            print("    S: Standard mode")
            print("    L: Limited shots mode")
            print("    V: Versus other player")
            print()
            print("    Q: Quit")
            print()
            user_input = input("    Enter: ").upper()
            print()
            if user_input not in menu_triggers:
                print("\nWrong input!\n")
                continue
            print("\n" * 10)
            menu_triggers[user_input]()


if __name__ == "__main__":
    sb = SeaBattle()
    sb.main_menu()
