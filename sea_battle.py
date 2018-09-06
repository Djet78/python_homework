from random import randint
from copy import deepcopy


class SeaBattle:

    limited_shots_mode = False
    in_game = False

    def _user_input_handler(self, lower_bound, higher_bound, message=""):
        in_game_commands = {"Q": self._quit, "H": self._help}
        while True:
            uinput = input("    Enter{}: ".format(message)).upper()
            print()
            try:
                if self.in_game and uinput in in_game_commands:
                    in_game_commands[uinput]()
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
        print("Write amount of ships.")
        print("There can be no less than 1, and no more then {}!".format(amount_of_tiles - 1))
        print()
        ships_amount = self._user_input_handler(1, amount_of_tiles - 1, " ships quantity")
        print("\n" * 10)
        return ships_amount

    def _set_shots(self, ships_amount, amount_of_tiles):
        print("Amount of shots can`t be less than ships amount: {}, and bigger then tiles amount: {}!"
              .format(ships_amount, amount_of_tiles))
        shots = self._user_input_handler(ships_amount, amount_of_tiles, " shots amount")
        print("\n" * 10)
        return shots

    def _generate_empty_field(self, horizontal, vertical):
        field = [["0" for _ in range(horizontal + 1)]for _ in range(vertical + 1)]
        field[0] = [str(int(x) + i) for i, x in enumerate(field[0])]
        for idx in range(len(field)):
            field[idx][0] = str(int(field[idx][0]) + idx)
        field[0][0] = "*"
        return field

    def _add_ships_on_field(self, ships, field):
        while ships:
            for hor, row in enumerate(field):
                if hor == 0:
                    continue
                for ver, cell in enumerate(row):
                    if ships == 0:
                        break
                    if cell == "0" and randint(0, 100) > 60:
                        ships -= 1
                        field[hor][ver] = "1"
        return field

    def _set_game_options(self):
        horizontal, vertical = self._set_field_params()
        amount_of_tiles = horizontal * vertical
        ships_amount = self._set_ship_amount(amount_of_tiles)
        user_field = self._generate_empty_field(horizontal, vertical)
        battle_field = self._add_ships_on_field(ships_amount, deepcopy(user_field))
        shots = None
        if self.limited_shots_mode:
            shots = self._set_shots(ships_amount, amount_of_tiles)
        self._game_process(battle_field, user_field, ships_amount, shots)

    def _limited_shots_mode_trigger(self):
        self.limited_shots_mode = True
        self._set_game_options()

    def _game_process(self, battle_field, user_field, ships_amount, shots):
        self.in_game = True
        max_hor_value = len(user_field) - 1
        max_ver_value = len(user_field[0]) - 1
        if shots is None:
            shots = "Unlimited"
        while ships_amount and shots:
            print("Type 'h' for help, or 'q' for quit")
            print("\n" * 3)
            print("Shots: {}".format(shots))
            for line in user_field:
                print(line)
            print()
            print("Shot to:")
            hor = self._user_input_handler(1, max_hor_value, " horizontal")
            ver = self._user_input_handler(1, max_ver_value, " vertical")
            if battle_field[hor][ver] == "0":
                user_field[hor][ver] = "~"
            else:
                if user_field[hor][ver] != "X":
                    ships_amount -= 1
                    user_field[hor][ver] = "X"
            if isinstance(shots, int):
                shots -= 1
        print("\n" * 10)
        if ships_amount == 0:
            print("    Win! You have destroyed last ship!")
        else:
            print("    Sorry, you lose! You have no more shots!")
        print("\n" * 5)

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
        self.in_game = False
        menu_triggers = {"Q": self._quit, "S": self._set_game_options,
                         "L": self._limited_shots_mode_trigger}
        while True:
            print()
            print("Type: For:")
            print("    S: Standard mode")
            print("    L: Limited shots mode")
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
    print("        Welcome to sea battle!")
    sb.main_menu()
