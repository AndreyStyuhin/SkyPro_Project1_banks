import json
from typing import Any, Dict

from src.utils import (get_card_with_spend, get_currency, get_data_time,
                       get_path_and_period, get_stock, get_time_for_greeting,
                       get_top_transactions)


def main_info(date_time: str) -> Dict[str, Any]:
    """
    функций и главную функцию, принимающую на вход строку с датой и временем
    в формате YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ
    :param date_time: 2022-01-01 12:00:00
    :return: {
        "year": 2022,
        "month": 1,
        "day": 1,
        "hour": 12,
        "minute": 0,
        "second": 0
    """

    # Делаем срез всего файла xlsx по диапазону даты
    time_period = get_data_time(date_time)
    sorted_df = get_path_and_period("../data/operations.xlsx", time_period)

    # 1. Приветствие
    greeting = get_time_for_greeting()

    # 2. Вывод по каждой карте
    cards = get_card_with_spend(sorted_df)

    # 3. Топ-5 транзакций по сумме платежа
    top_transactions = get_top_transactions(sorted_df, 5)

    # 4. Курс валют
    currency_rates = get_currency("../data/user_settings.json")

    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
    }

    # 5. Стоимость акция из S&P500
    stock_prices = get_stock("../data/user_settings.json")

    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data
