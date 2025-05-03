from pandas import DataFrame
import pandas as pd


def spending_by_category(transactions: pd.DataFrame, category: str, date: str) -> dict:
    """
    функция, которая принимает таблицу и возвращает словарь с
    расходами по категориям за последние три месяца
    :param df:
    :return:
    """
    print(transactions)
    #expenses_by_category = df.groupby("Категория")["Сумма операции"].sum()
    #return expenses_by_category.to_dict()