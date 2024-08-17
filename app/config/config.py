__author__ = 'Alexey Manikin'

import os

from dotenv import load_dotenv

load_dotenv()

# Default logger
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/../')

MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_PORT = int(os.environ["MYSQL_PORT"])
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PASSWD = os.environ["MYSQL_PASSWD"]
MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]

TELEGRAM_BOT_KEY = os.environ["TELEGRAM_BOT_KEY"]

TELEGRAM_BOT_HELP = """Commands for the Telegram bot that simplifies financial tracking:

* Incomes: uploading official incomes in PDF format (under development)
* Expenses: entered in a free form with the purpose, amount, and date (if the expense did not occur today):
  - Example: "Filled up the car with 100 euros."
  - Example: "bread - 5.50"
  - Example: "paid Ivanov salary 200"
* Additional incomes: entered with a note such as "received", "earned", etc.:
  - Example: "earned 200"
* Additional commands:
    /print_group - displays a list of groups
    /summary - shows total expenses over the last 30 days
    /last - displays the last entries over the last 30 days"""
