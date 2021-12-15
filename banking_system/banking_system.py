import itertools
import random
import sqlite3

class WrongInputException(Exception):
    # main class for exceptions
    ...

class IsNotNumber(Exception):
    ...


class BankingSystem:
    MAIN_MENU = """
        1. Create an account
        2. Log into account
        0. Exit
        """
    CARD_MENU = """
        1. Balance
        2. Add income
        3. Do transfer
        4. Close account
        5. Log out
        0. Exit
        """

    def __init__(self):
        self.menu = self.MAIN_MENU
        self.state = 1
        self.card = None
        self.card_transfer = None
        self.db = sqlite3.connect('db_cards.s3db')
        self.cur = self.db.cursor()

    def db_create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0)""")
        self.db.commit()

    def make_action(self, action):
        if action == "1" and self.state == 1:
            self.generate_card_number()
            return self.show_menu()
        elif (action == "2" and self.state == 1) or (action != 0 and self.state in (2, 3)):
            return self.log_in()
        elif self.state in (4, 5, 6, 7):
            return self.balance_menu(action)
        elif action == "0":
            print("Bye!")
            exit()

    def show_menu(self):
        return self.menu

    def show_card_menu(self):
        self.state = 4
        return self.CARD_MENU

    def check_input(self, action):
        try:
            if action.isnumeric() is False:
                raise IsNotNumber
        except IsNotNumber:
            print("You should enter numbers!")
            return True
        else:
            ...
        finally:
            ...

    def generate_card_number(self):
        card_num = random.randint(0000000000, 9999999999)
        card_num = int(str(400000) + str(card_num))
        if self.luna(card_num) is True:
            print(f"""
            Your card has been created
            Your card number:
            {card_num}""")
            self.generate_pin_code(card_num)
        else:
            self.generate_card_number()

    def luna(self, card_num):
        card_num = list(map(int, str(card_num)))
        card_num = [p * 2 if i % 2 else p for i, p in enumerate(card_num, 1)]
        for i, p in enumerate(card_num, 0):
            if p > 9:
                p = list(map(int, str(p)))
                card_num[i] = sum(p)
        card_num_sum = sum(card_num)
        if card_num_sum % 10 == 0:
            return True
        else:
            return False

    def generate_pin_code(self, card_num):
        pin = random.randint(0000, 9999)
        print(f"""
        Your card PIN:
        {pin}""")
        self.db_insert_card_pin(card_num, pin)

    def log_in(self):
        if action == "2":
            self.state = 2
            return "Enter your card number: "
        elif action != "2" and self.state == 2:
            if self.check_input(action) is True:
                return "Enter your card number: "
            else:
                card = self.db_select_card_number(action)
                if card is None:
                    return "Card is incorrect. Enter again your card number: "
                elif action == card[0]:
                    self.card = action
                    self.state = 3
                    return "Enter your PIN: "
        elif action != "2" and self.state == 3:
            if self.check_input(action) is True:
                return "Enter your PIN: "
            else:
                pin = self.db_select_pin()
                if action == pin[0]:
                    return "You have successfully logged in!" + self.show_card_menu()
                else:
                    return "PIN is incorrect. Enter again your PIN: "

    def balance_menu(self, action):
        if action == "4" and self.state == 4:
            self.db_delete_line()
            self.state = 1
            return "The account has been closed!" + self.show_menu()
        elif action == "5" and self.state == 4:
            self.state = 1
            return "You have successfully logged out!" + self.show_menu()
        elif action == "0":
            print("Bye!")
            exit()
        elif action == "1":
            return self.current_balance()
        elif action == "2" or self.state == 5:
            return self.balance_income()
        elif action == "3" or self.state in (6, 7):
            return self.transfer()

    def current_balance(self):
        balance = self.db_select_balance()
        return f"Balance is {balance[0]}" + self.CARD_MENU

    def balance_income(self):
        if action == "2":
            self.state = 5
            return "Enter Income: "
        elif self.state == 5:
            if self.check_input(action) is True:
                return "Enter correct Income: "
            else:
                income = self.db_select_balance()
                income = int(income[0]) + int(action)
                self.db_update_balance(income)
                self.state = 1
                return "Income was added!" + self.show_card_menu()

    def transfer(self):
        if action == "3":
            self.state = 6
            return "Transfer! Enter card number: "
        elif self.state == 6:
            if self.check_input(action) is True:
                return "Card is incorrect. Enter again your card number: "
            else:
                card = self.db_select_card_number(action)
                if card is None:
                    return "Such a card does not exist. Enter again your card number: "
                elif self.card == action:
                    return "You can't transfer money to the same account. Enter another card: "
                elif action == card[0]:
                    self.card_transfer = action
                    self.state = 7
                    return "Enter how much money you want to transfer: "
        elif self.state == 7:
            available_balance = self.db_select_balance()
            if int(action) <= int(available_balance[0]):
                self.db_transfer_balance(available_balance, action)
                self.state = 4
                return "Success!" + self.show_card_menu()
            elif int(action) > int(available_balance[0]):
                return "Not enough money! Enter another sum of transfer: "

    def db_insert_card_pin(self,card_num,pin):
        self.cur.execute(f"INSERT INTO cards(number, pin) VALUES({card_num}, {pin})")
        self.db.commit()

    def db_select_card_number(self,action):
        self.cur.execute(f"SELECT number FROM cards WHERE number = {action}")
        return self.cur.fetchone()

    def db_select_pin(self):
        self.cur.execute(f"SELECT pin FROM cards WHERE number = {self.card}")
        return self.cur.fetchone()

    def db_delete_line(self):
        return self.cur.execute(f"DELETE FROM cards WHERE number = {self.card}")

    def db_select_balance(self):
        self.cur.execute(f"SELECT balance FROM cards WHERE number = {self.card}")
        return self.cur.fetchone()

    def db_update_balance(self, income):
        self.cur.execute(f"UPDATE cards SET balance = {income} WHERE number = {self.card}")
        self.db.commit()

    def db_transfer_balance(self, available_balance, action):
        self.cur.execute(f"UPDATE cards SET balance = {int(available_balance[0]) - int(action)}")
        self.db.commit()


bank = BankingSystem()
bank.db_create_table()
bank_response = bank.show_menu()


def bruteforce_card():
    generator = itertools.product('1234567890', repeat=10)
    for card in generator:
        card = str(''.join(card))
        card = str(400000) + str(card)
        yield card


def bruteforce_pin():
    generator = itertools.product('1234567890', repeat=4)
    for password in generator:
        pin = str(''.join(password))
        yield pin


card = bruteforce_card()
pin = bruteforce_pin()

while True:
    action = input(bank_response)
    bank_response = bank.make_action(action)
    while bank_response == "Card is incorrect. Enter again your card number: ":
        action = next(card)
        bank_response = bank.make_action(action)
    while bank_response == "PIN is incorrect. Enter again your PIN: ":
        action = next(pin)
        bank_response = bank.make_action(action)

