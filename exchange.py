import os
import ast
import json
import requests
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import date, timedelta
from bs4 import BeautifulSoup

from settings import LATEST_EXCHANGES_URL, MAX_DIFF_IN_SEC, HISTORY_URL_TEMPLATE, HISTORY_PNG_FILE
from database import get_data_from_database, save_data_to_database


def get_latest_rates():
    database_ts, database_rates = get_data_from_database()

    # check current timestamp with local database
    cur_ts = datetime.datetime.now().timestamp()
    # calculate the timestamp difference
    diff = cur_ts - database_ts

    # check that the timestamp difference is lower then 10 minutes
    if diff <= MAX_DIFF_IN_SEC:
        return database_rates

    # get all rates data from website
    response = requests.get(LATEST_EXCHANGES_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    exhanges_info = ast.literal_eval(soup.get_text())
    rates = exhanges_info["rates"]
    date = exhanges_info["date"]

    exhanges_list = list()
    for key, value in rates.items():
        exhanges_list.append((key, round(value, 2)))

    save_data_to_database(exhanges_list)

    return exhanges_list


def exchange_to_another_currency(amount_of_usd, currency_name):
    current_rates = get_latest_rates()
    currency_coef = list(
        filter(lambda currency: currency[0] == currency_name, current_rates))[0][1]
    return round(amount_of_usd * currency_coef, 2)


def get_history(currency_name, history_len_in_days):
    history_url = HISTORY_URL_TEMPLATE.format(
        date.today() - timedelta(days=history_len_in_days), date.today(), currency_name)

    response = requests.get(history_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    history_info = ast.literal_eval(soup.get_text())
    rates = history_info["rates"]

    rates_items = rates.items()
    if len(rates_items) < history_len_in_days:
        return []

    sorted_items = sorted(rates_items,
                          key=lambda item: datetime.datetime.strptime(item[0], "%Y-%m-%d").date())

    return [(datetime.datetime.strptime(item[0], "%Y-%m-%d").date(), list(item[1].values())[0]) for item in sorted_items]


def save_history_to_debug_file(history_rates):
    ax = plt.gca()
    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = mdates.DayLocator()
    ax.xaxis.set_major_locator(locator)

    print(history_rates)
    x_values, y_values = zip(*history_rates)
    plt.plot(x_values, y_values)

    if os.path.exists(HISTORY_PNG_FILE):
        os.remove(HISTORY_PNG_FILE)
    plt.savefig(HISTORY_PNG_FILE)
    plt.close()
