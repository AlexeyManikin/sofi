__author__ = 'Alexey Y Manikin'

import datetime
import re
import traceback

import telebot

import classes.bill_parser
import classes.llm_parser
import classes.read_pdf
from config import config

botTelegram = telebot.TeleBot(config.TELEGRAM_BOT_KEY)


@botTelegram.message_handler(commands=['start'])
def start_bot(message: telebot.types.Message):
    botTelegram.reply_to(message, config.TELEGRAM_BOT_HELP)


@botTelegram.message_handler(commands=['print_group'])
def print_group(message: telebot.types.Message):
    model = classes.llm_parser.LLMParser()
    result = ""
    for item in model.get_list_of_category():
        result += " - " + str(model.get_list_of_category()[item]) + "\n"
    botTelegram.reply_to(message, result)


@botTelegram.message_handler(commands=['summary'])
def summary(message: telebot.types.Message):
    model = classes.llm_parser.LLMParser()
    count_days = 365
    result = model.get_summary_row(count_days)
    return_str = f"Суммарные данные за последние {count_days} дней:\n" + \
                 f" - траты             {result['summ']} euro\n" + \
                 f" - prompt_tokens     {result['prompt_tokens']} tokens\n" + \
                 f" - total_tokens      {result['total_tokens']} tokens\n" + \
                 f" - completion_tokens {result['completion_tokens']} tokens\n" + \
                 f" - elapsed_time      {result['elapsed_time']} seconds"

    botTelegram.reply_to(message, return_str)


@botTelegram.message_handler(commands=['last'])
def last(message: telebot.types.Message):
    model = classes.llm_parser.LLMParser()
    result = model.get_list_spending(30)
    str_result = ""
    for item in result:
        str_result += " - " + str(item['date'])[0:10] + " - " + \
                      str(model.get_list_of_category()[item['group_type']]) + " - " + str(item['description']) + \
                      " - " + str(item['summ']) + "\n"

    botTelegram.reply_to(message, str_result)


@botTelegram.message_handler(content_types=['text'])
def parce_message(message: telebot.types.Message):
    try:
        if not re.findall(r'\d+', message.text):
            return

        model = classes.llm_parser.LLMParser()
        result = model.parse_date(message.text, message.date, message.from_user.full_name)

        if result != {}:
            d = model.get_list_of_category()
            try:
                group = d[result['group']]
            except KeyError:
                group = result['group']

            return_text = "Данные добавлены: \n" + \
                          "  - сумма: %s\n" % result['summ'] + \
                          "  - группа: %s\n" % group + \
                          "  - описание: %s\n" % result['description'] + \
                          "  - дата: %s\n" % result['date'] + \
                          "  - обоснование: %s\n" % result['reasoning']
            botTelegram.reply_to(message, return_text)
    except Exception as e:
        print((traceback.format_exc()))
        botTelegram.reply_to(message, e)


@botTelegram.message_handler(content_types=['document'])
def handle_docs_pdf(message: telebot.types.Message):
    try:
        # пока не особо работает надо сидеть править regexp - это где-то на 2 дня занятие
        file_info = botTelegram.get_file(message.document.file_id)
        downloaded_file = botTelegram.download_file(file_info.file_path)

        new_file_name = (config.CURRENT_PATH + '/pdf_data/txt/' +
                         datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S') +
                         "_" + str(message.chat.id) + ".txt")

        with open(new_file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        parser = classes.bill_parser.BillParser()
        result = parser.run(new_file_name)

        return_message = "Я сохранил этот файл: : %s\n" % new_file_name + \
                         " - вставлено новых чеков: %s\n" % result["count_bills"] + \
                         " - вставлено новых блюд: %s\n" % result["count_dish"] + \
                         " - найденно существующих записей: %s\n" % result["count_bills_already_insert"]

        botTelegram.reply_to(message, return_message)
    except Exception as e:
        print((traceback.format_exc()))
        botTelegram.reply_to(message, e)


def run():
    botTelegram.infinity_polling()
