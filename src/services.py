import json

import pandas as pd


def anylize_cashback(file_path: str, year: int, month: int) -> dict[str, int]:
    """
    Анализирует выгодные категории кэшбэка
    и возвращает json
    :return:
    """
    df = pd.read_excel(file_path)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    filtered_data = df[
        (df["Дата операции"].dt.year == year) &
        (df["Дата операции"].dt.month == month)
    ]
    filtered_data = filtered_data[
        (filtered_data["Кэшбэк"] > 0)
    ]
    filtered_data = filtered_data[
        filtered_data["Сумма платежа"] < 0
    ]

    expenses_by_category = (filtered_data.groupby("Категория")["Сумма платежа"].sum())
    cashback_by_category = (abs(expenses_by_category)) //100

    #print(cashback_by_category)
    result = cashback_by_category.to_dict()
    return json.dumps(result, ensure_ascii=False, indent=4)

    # Здесь должен быть код для формирования и возврата результата
    #return {}  # Заглушка

