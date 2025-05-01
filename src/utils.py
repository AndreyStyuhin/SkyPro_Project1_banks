import json
from datetime import datetime

import pandas as pd
import requests
from pandas import DataFrame
from pandas.core.computation.common import result_type_many

URL = "https://api.apilayer.com/currency_data/convert"
API_KEY = "GCGafly8aQO9QhrYCEpjIdF14EixNCqI"

API_KEY_STOCK = "1c2c542c62cdcc57513d86f2f38f290c"  # ← API ключ stock!
BASE_URL = "http://api.marketstack.com/v1/eod"
URL_STOCK = f"{BASE_URL}?access_key={API_KEY_STOCK}&symbols=AAPL"


def get_time_for_greeting():
    """
    функция, которая возвращает "Доброе утро" / "Добрый день"
    / "Добрый вечер" / "Доброй ночи" в зависимости от времени суток.
    :return:
    """
    user_datetime_hour = datetime.now().hour
    if 5 <= user_datetime_hour < 12:
        return "Доброе утро"
    elif 12 <= user_datetime_hour < 18:
        return "Добрый день"
    elif 18 <= user_datetime_hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_data_time(date_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]:
    """
    функция, которая возвращает текущую дату и время в формате
    YYYY-MM-DD HH:MM:SS
    :return:
    """
    dt = datetime.strptime(date_time, date_format)
    start_of_month = dt.replace(day=1)

    return [
        start_of_month.strftime("%d.%m.%Y %H:%M:%S"),
        dt.strftime("%d.%m.%Y %H:%M:%S")
    ]


def get_path_and_period(path_to_file: str, period_date: list) -> DataFrame:
    """
    функция, которая принимает путь к файлу, список дат, и возвращает
    таблицу в заданном периоде
    :param path_to_file:
    :param period_date:
    :return:
    """
    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
    ]
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    return sorted_df


def get_card_with_spend(sorted_df: DataFrame) -> list[dict]:
    """
    функция, которая принимает отсортированную таблицу и возвращает таблицу с
    операциями по карте
    :param sorted_df:
    :return:
    """
    card_spent_transactions = []
    card_sorted = sorted_df[
        [
            "Номер карты",
            "Сумма операции",
            "Кэшбэк",
            "Сумма операции с округлением",
        ]
    ]
    for index, row in card_sorted.iterrows():
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"]).replace("*", "")
            total_spend = row["Сумма операции с округлением"]
            cashback = total_spend // 100
            row = {
                "last_digits": last_digits,
                "total_spend": total_spend,
                "cashback": cashback
            }
            card_spent_transactions.append(row)
    return card_spent_transactions


def get_top_transactions(sorted_df: DataFrame, get_top):
    """
    функция, которая принимает отсортированную таблицу и
    возвращает топ(get_top) таблицу с
    операциями по сумме платежа

    """
    top_pay_transactions = []
    sorted_pay_df = sorted_df.sort_values(by="Сумма операции", ascending=False)
    top_transactions = sorted_pay_df.head(get_top)
    top_transactions_sorted = top_transactions[
        [
            "Дата платежа",
            "Сумма операции",
            "Категория",
            "Описание"
        ]
    ]
    for index, row in top_transactions_sorted.iterrows():
        transaction = {
        "date": f"{row['Дата платежа']}",
        "amount": f"{row['Сумма операции']}",
        "category": f"{row['Категория']}",
        "description": f"{row['Описание']}",
        }
        top_pay_transactions.append(transaction)
    return top_pay_transactions


def get_currency(path_to_json: str) -> list[dict]:
    """
    функция, которая принимает путь к файлу с настройками и возвращает словарь с
    текущим курсом валют
    :param path_to_json:
    :return:
    """
    currency_rates = []
    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        currences = data['user_currencies']

        for currency in currences:
            params = {
                "amount": 1,
                "from": f"{currency}",
                "to": "RUB"
            }
            headers = {
                "apikey": f"{API_KEY}"
            }
            responses = requests.request("GET", URL, headers=headers, data=params)

            status_code = responses.status_code
            if status_code == 200:
                result = responses.json()
                currency_code_response = result['query']['from']
                currency_amount = round(result['result'], 2)
                currency_rates.append({
                    "currency": f"{currency_code_response}",
                    "rate": f"{str(currency_amount)}"
                })
        return currency_rates


def get_stock(path_to_json: str) -> list[dict]:
    """
    функция, которая принимает путь к файлу с настройками и возвращает словарь с
    текущим курсом акций
    :param path_to_json:
    :return:
    """
    try:
        # Загружаем настройки из JSON
        with open(path_to_json, "r", encoding="utf-8") as file:
            data = json.load(file)
            stocks = data.get('user_stocks', [])

        if not stocks:
            return []

        # Формируем URL запроса
        symbols = ",".join(stocks)
        url = f"http://api.marketstack.com/v1/eod?access_key={API_KEY_STOCK}&symbols={symbols}"

        # Отправляем запрос
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Обрабатываем ответ
        stock_prices = []
        if "data" in data:
            for stock_data in data["data"]:
                if "symbol" in stock_data and "close" in stock_data:
                    stock_prices.append({
                        "stock": stock_data["symbol"],
                        "price": stock_data["close"]
                    })

        return stock_prices

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return []
    except ValueError as e:
        print(f"Ошибка при обработке JSON: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return []
