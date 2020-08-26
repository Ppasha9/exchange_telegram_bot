import json
import datetime

from settings import DATABASE_FILE


def get_data_from_database():
    with open(DATABASE_FILE, "r") as f:
        database_obj = json.load(f)
    database_ts = database_obj["timestamp"]
    database_rates = database_obj["rates"]

    return database_ts, database_rates


def save_data_to_database(rates_to_save):
    ts = datetime.datetime.now().timestamp()
    obj_to_save = {
        "timestamp": ts,
        "rates": rates_to_save,
    }

    with open(DATABASE_FILE, "w") as f:
        json.dump(obj_to_save, f)
