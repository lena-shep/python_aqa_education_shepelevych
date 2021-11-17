import logging.config
import time


class WrongInputException(Exception):
    # main class for exceptions
    ...


class InputIsNumber(WrongInputException):
    # class for exceptions when input is not number
    ...


class InputIsInRange(WrongInputException):
    # class for exceptions when input is not in range
    ...


class Game:
    def __init__(self, *args):
        self.menu = """
        1 - Play
        2 - Show the log
        3 - Clear the log
        4 - Exit
        """
        self.table = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        self.state = 0
        self.player = 1
        self.sign = "X"
        self.list_index = None
        self.names = []
        self.user_name_index = None

    def __print_table(self):
        print(" _________", "\n", "|", self.table[0], self.table[1], self.table[2], "|", "\n",
              "|", self.table[3], self.table[4], self.table[5], "|", "\n",
              "|", self.table[6], self.table[7], self.table[8], "|", "\n",
              "_________")

    def start(self):
        return self.menu

    def take_action(self, *args):
        if user_step == "1" or self.state in (1, 2, 3):
            return self.play_game()
        elif user_step == "2":
            with open("app.log", "r") as f:
                print(f.read())
                exit()
        elif user_step == "3":
            with open("app.log", "r+") as f:
                f.truncate()
                exit()
        elif user_step == "4":
            exit()

    def play_game(self):
        if self.state in (0, 1):
            return self.ask_names()
        elif self.state == 2:
            return self.play_round()
        elif self.state == 3 and user_step == "Y":
            self.table = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
            self.state = 2
            self.user_name_index = 1
            self.__print_table()
            return f"{self.names[self.user_name_index]}, your step. Choose cell coordinates: "
        elif self.state == 3 and user_step == "N":
            exit()

    def ask_names(self):
        if self.names.__len__() == 0 and self.state == 0:
            self.state = 1
            return "First player, please, enter your name - "
        elif self.names.__len__() == 0 and self.state == 1:
            self.names.append(user_step)
            return "Second player, please, enter your name - "
        elif self.names.__len__() == 1:
            self.names.append(user_step)
            self.__print_table()
            self.state = 2
            self.user_name_index = 0
            return f"{self.names[self.user_name_index]}, your step. Choose cell coordinates: "

    def timer(func):
        def wrapper(self):
            start = time.time()
            result = func(self)
            end = time.time()
            duration = end - start
            logger.info(f"Game takes {duration} seconds")
            return result
        return wrapper

    @timer
    def play_round(self):
        if self.check_user_input() is True:
            return "Choose another cell! "
        else:
            self.state = 2
        user_step_list = user_step
        user_step_list = user_step_list.split()
        i = int(user_step_list[0])
        j = int(user_step_list[1])
        self.list_index = (i - 1) * 3 + j - 1
        if self.player in (1, 2) and self.table[:].count("_") != 0:
            self.choose_sign()
            if self.table[self.list_index] in ("X", "0"):
                return "This cell is occupied! Choose another one! "
            self.table[self.list_index] = self.sign
            self.__print_table()
            self.check_result()
            self.player = 2 if self.player == 1 else 1
            if self.__bool__() is True:
                self.state = 3
                return "Do you want to play again? Y/N "
            else:
                self.user_name_index = 1 if self.user_name_index == 0 else 0
                return f"{self.names[self.user_name_index]}, your step. Choose cell coordinates: "

    def choose_sign(self):
        self.sign = "X" if self.player == 1 else "0"

    def check_user_input(self, *args):
        user_step_list = user_step
        user_step_list = user_step_list.split()
        try:
            if user_step_list[0].isnumeric() is False or user_step_list[1].isnumeric() is False:
                raise InputIsNumber
            if user_step_list[0] not in ("1", "2", "3") or user_step_list[1] not in ("1", "2", "3"):
                raise InputIsInRange
        except InputIsNumber:
            print("You should enter numbers!")
            logger.error("You should enter numbers!")
            return True
        except InputIsInRange:
            print("Coordinates should be from 1 to 3!")
            logger.error("Coordinates should be from 1 to 3!")
            return True
        else:
            ...
        finally:
            ...

    def __bool__(self):
        return self.table[0:3].count(self.sign) == 3 or self.table[3:6].count(self.sign) == 3 or self.table[6:9].count(self.sign) == 3 or self.table[0:8:3].count(self.sign) == 3\
                or self.table[1:9:3].count(self.sign) == 3 or self.table[2:9:3].count(self.sign) == 3 or self.table[0:9:4].count(self.sign) == 3\
                or self.table[2:7:2].count(self.sign) == 3

    def check_result(self):
        if self.__bool__() is True:
            print(f"{self.names[self.user_name_index]} wins!")
            logger.info(f"{self.names[self.user_name_index]} is a winner")
        # Game not finished когда ни одна из сторон не имеет трех символов подряд, но на игровой сетке все еще есть пустые ячейки
        elif self.__bool__() is False and self.table[:].count("_") != 0:
            print("Game not finished")
        # Draw когда ни на одной стороне нет трех символов в ряд, а  на игровой сетке нет пустых ячеек
        elif self.__bool__() is False and self.table[:].count("_") == 0:
            print("Draw")
            logger.info("There is no winner")
            exit()
        # Impossible когда на игровой сетке три крестика “X” подряд,  а также три нолика “0” подряд или
        # # если крестиков “X” намного больше, чем ноликов “0” или наоборот
        elif (self.table[0:3].count("X") == 3 or self.table[3:6].count("X") == 3 or self.table[6:9].count("X") == 3
                or self.table[0:8:3] == "X" or self.table[1:9:3] == "X" or self.table[2:9:3] == "X" or self.table[0:9:4] == "X" or self.table[2:7:2] == "X")\
                and (self.table[0:3].count("0") == 3 or self.table[3:6].count("0") == 3 or self.table[6:9].count("0") == 3
                 or self.table[0:8:3] == "0" or self.table[1:9:3] == "0" or self.table[2:9:3] == "0" or self.table[0:9:4] == "X" or self.table[2:7:2] == "0"):
            print("Impossible")
            exit()
        elif ((self.table[:].count("X") - self.table[:].count("0")) >= 2) or ((self.table[:].count("0") - self.table[:].count("X")) >= 2):
            print("Impossible")
            exit()


if __name__ == "__main__":
    logging.config.fileConfig('logger.conf')
    logger = logging.getLogger("TicTacToe")

    game = Game()
    app_response = game.start()

    while True:
        user_step = input(app_response)
        app_response = game.take_action()


