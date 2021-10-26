class CoffeeMachine:
    ESPRESSO = {"WATER": 250, "MILK": 0, "BEANS": 16, "PRICE": 4}
    LATTE = {"WATER": 350, "MILK": 350, "BEANS": 20, "PRICE": 7}
    CAPPUCCINO = {"WATER": 200, "MILK": 100, "BEANS": 12, "PRICE": 6}

    def __init__(self, water, milk, beans, disposable_cups, money):
        self.water = water
        self.milk = milk
        self.beans = beans
        self.disposable_cups = disposable_cups
        self.money = money
        self.__water_for_cup = None
        self.__milk_for_cup = None
        self.__bean_for_cup = None
        self.__price_for_cup = None
        self.current_state = None
        self.coffee_type = "What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, 4 - back - "
        self.state_questions = 0
        self.questions = [
                "Write how many ml of water you want to add - ",
                "Write how many ml of milk you want to add - ",
                "Write how many grams of coffee beans you want to add - ",
                "Write how many disposable coffee cups you want to add - "
            ]
        self.ingredients = []
        self.start_response = "Write action (buy, fill, take, remaining, exit) - "

    def start(self):
        return self.start_response

    def take_action(self, *args):
        if action == "buy":
            self.current_state = "buy"
            return self.coffee_type
        elif self.current_state == "buy" and action in ("1", "2", "3", "4"):
            self.current_state = None
            self.buy_coffee(action)
        elif action == "fill" or self.current_state == "fill":
            self.current_state = "fill"
            if action == "fill":
                return self.questions[self.state_questions]
            elif 0 <= self.state_questions < 4:
                self.ingredients.append(int(action))
                self.state_questions += 1
                if self.state_questions < 4:
                    return self.questions[self.state_questions]
            self.current_state = None
            self.fill_machine(self.ingredients)
        elif action == "take":
            self.take_money()
        elif action == "remaining":
            self.available_ingredients()
        elif action == "exit":
            exit()
        return self.start_response

    def buy_coffee(self, *args):
        if action == "1":
            self.__water_for_cup = self.ESPRESSO.get("WATER")
            self.__milk_for_cup = self.ESPRESSO.get("MILK")
            self.__bean_for_cup = self.ESPRESSO.get("BEANS")
            self.__price_for_cup = self.ESPRESSO.get("PRICE")
            self.prepare_coffee()
        elif action == "2":
            self.__water_for_cup = self.LATTE.get("WATER")
            self.__milk_for_cup = self.LATTE.get("MILK")
            self.__bean_for_cup = self.LATTE.get("BEANS")
            self.__price_for_cup = self.LATTE.get("PRICE")
            self.prepare_coffee()
        elif action == "3":
            self.__water_for_cup = self.CAPPUCCINO.get("WATER")
            self.__milk_for_cup = self.CAPPUCCINO.get("MILK")
            self.__bean_for_cup = self.CAPPUCCINO.get("BEANS")
            self.__price_for_cup = self.CAPPUCCINO.get("PRICE")
            self.prepare_coffee()

    def prepare_coffee(self):
        if self.water >= self.__water_for_cup and self.milk >= self.__milk_for_cup and self.beans >= self.__bean_for_cup and self.disposable_cups >= 1:
            print("I have enough resources, making you a coffee!")
            self.water -= self.__water_for_cup
            self.milk -= self.__milk_for_cup
            self.beans -= self.__bean_for_cup
            self.disposable_cups -= 1
            self.money += self.__price_for_cup
        elif self.water < self.__water_for_cup:
            print("Sorry, not enough water!")
        elif self.milk < self.__milk_for_cup:
            print("Sorry, not enough milk!")
        elif self.beans < self.__bean_for_cup:
            print("Sorry, not enough beans!")
        elif self.disposable_cups < 1:
            print("Sorry, not enough disposable cups!")
        return self.water, self.beans, self.disposable_cups, self.money

    def fill_machine(self, *args):
        self.water += self.ingredients[0]
        self.milk += self.ingredients[1]
        self.beans += self.ingredients[2]
        self.disposable_cups += self.ingredients[3]
        self.available_ingredients()
        return self.water, self.milk, self.beans, self.disposable_cups

    def take_money(self):
        print("I gave you - %d" % self.money)
        self.money = 0
        self.available_ingredients()

    def available_ingredients(self):
        print("""
        The coffee machine has:
        %d of water
        %d of milk
        %d of coffee beans
        %d of disposable cups
        %d of money
        """ % (self.water, self.milk, self.beans, self.disposable_cups, self.money))
        return self.water, self.milk, self.beans, self.disposable_cups, self.money


machine = CoffeeMachine(400, 540, 120, 9, 550)
machine_response = machine.start()
while True:
    action = input(machine_response)
    machine_response = machine.take_action(action)



