import os
import re
from collections import deque
import requests
import sys
from bs4 import BeautifulSoup
from colorama import Fore, Style


class WrongURL(Exception):
    ...


class Browser:

    def __init__(self):
        self.menu = "Enter URL: "
        self.queue = deque()

    def show_menu(self):
        return self.menu

    def take_action(self, action):
        if action == "exit":
            exit()
        elif action == "back":
            return self.back_button(action)
        elif action.__contains__("."):
            self.queue.append(action)
            action = self.add_https(action)
            r = requests.get(action)
            self.print_page_content(r)
            self.create_file_in_package(action, r)
            return "\n" + self.menu
        elif self.check_url() is False:
            return self.open_file(action)
        else:
            return "Try again: "

    def back_button(self, action):
        if len(self.queue) == 0:
            exit()
        else:
            action = self.queue.pop()
            action = self.add_https(action)
            r = requests.get(action)
            self.print_page_content(r)
            return "\n" + self.menu

    def print_page_content(self, r):
        soup = BeautifulSoup(r.content, "html.parser")
        for i in soup.find_all(["p", "a", "ul", "ol", "li", "link"]):
            if i.get("href"):
                print(Fore.BLUE + i.get_text() + Style.RESET_ALL)
            else:
                print(i.get_text())

    def add_https(self, action):
        if re.search(r"https://", action) is None:
            action = "https://" + action
        return action

    def create_file_in_package(self, action, r):
        if re.search(r"https://", action) is not None:
            action = action.replace("https://", "")
        file = self.create_file_name(action)
        b_file = open(f"./browser/{str(sys.argv[1])}/{file}", "w+")
        b_file.write(r.text)
        b_file.close()

    def create_file_name(self, action):
        file_name = action
        file_name = file_name.split(sep=".")
        return file_name[0]

    def open_file(self, action):
        file = open(f"./browser/{str(sys.argv[1])}/{action}", "r")
        for line in file:
            print(line)
        return self.menu

    def check_url(self, *args):
        try:
            if os.access(f"./browser/{str(sys.argv[1])}/{action}", os.F_OK) is False and "." not in action:
                raise WrongURL
        except WrongURL:
            print("Error: URL should contain dot")
            return True
        else:
            return False


if __name__ == "__main__":
    try:
        if os.access(f"./browser/{str(sys.argv[1])}", os.F_OK):
            raise FileExistsError
    except FileExistsError:
        print("Package with such name already exists")
    else:
        os.mkdir(f"./browser/{str(sys.argv[1])}", mode=0o777)

    browser = Browser()
    browser_response = browser.show_menu()
    while True:
        action = input(browser_response)
        browser_response = browser.take_action(action)



