import re
import telebot

from settings import HISTORY_PNG_FILE
from exchange import get_latest_rates, exchange_to_another_currency, get_history, save_history_to_debug_file

bot = telebot.TeleBot('1300958382:AAFk8RX3pj52_z7aOXjIB0C9UEymBNd24Y0')

_exchange_pattern = re.compile(r'/exchange \d+ USD to \D+')
_history_pattern = re.compile(r'/history USD/\D+ for \d+ days')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Hello! This is test exchange bot!\n'
                     'Base currency is USD.\n'
                     'Supported commands:\n'
                     '  `/list or /lst` - returns list of all latest exchange rates.\n'
                     '  `/exchange 10 USD to CAD` - converts currency to the second currency.\n'
                     '  `/history USD/CAD for 7 days` - return an image graph chart which shows the exchange rate graph/chart of the selected currency for the last 7 days.\n',
                     parse_mode='Markdown')


@bot.message_handler(commands=['list', 'lst'])
def list_message(message):
    latest_rates = get_latest_rates()
    bot_message = "Latest exchange rates (base is <b>USD</b>):\n"
    for rate in latest_rates:
        bot_message += "    <b>{}</b>: {}\n".format(*rate)

    bot.send_message(message.chat.id, bot_message, parse_mode='html')


@bot.message_handler(commands=['exchange'])
def exchange_message(message):
    if not _exchange_pattern.match(message.text):
        bot.send_message(
            message.chat.id, "Invalid /exchange command. Example: <b><i>/exchange 10 USD to CAD</i></b>", parse_mode='html')
        return

    splitted = message.text.split()
    usd_amount = int(splitted[1])
    currency_name = splitted[4]

    res = exchange_to_another_currency(usd_amount, currency_name)
    bot.send_message(message.chat.id, "Converted currency is: {} <b>{}</b>".format(
        res, currency_name), parse_mode='html')


@bot.message_handler(commands=['history'])
def history_message(message):
    if not _history_pattern.match(message.text):
        bot.send_message(
            message.chat.id, "Invalid /history command. Example: <b><i>/history USD/CAD for 7 days</i></b>", parse_mode='html')
        return

    splitted = message.text.split()
    currency_name = splitted[1][4:]
    history_days = int(splitted[3])

    history_rates = get_history(currency_name, history_days)
    if not history_rates:
        bot.send_message(
            message.chat.id, "No exchange rate data is available for the selected currency")
        return

    save_history_to_debug_file(history_rates)

    photo = open(HISTORY_PNG_FILE, 'rb')
    bot.send_photo(message.chat.id, photo)


bot.polling(none_stop=True)
