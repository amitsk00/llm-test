import configparser
import os
from colorama import Fore, Style

# Get the base directory of the current Python file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE)


def printInBox(msg):
    print("-------------------------------")
    print(Fore.RED + msg + Style.RESET_ALL)
    print("-------------------------------")


