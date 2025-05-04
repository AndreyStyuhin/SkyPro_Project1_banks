import functools
import json
import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def report_to_file(func):
    """
    Декоратор, который записывает возвращаемое значение функции в файл.
    Если имя файла не указано, используется имя по умолчанию.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # Проверяет, было ли указано в kwargs имя файла
        filename = kwargs.pop('filename', None)

        if filename is None:
            # Создает имя файла по умолчанию
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{func.__name__}_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(result, (pd.DataFrame, pd.Series)):
                    json.dump(result.to_dict(), f, ensure_ascii=False, indent=4)
                else:
                    json.dump(result, f, ensure_ascii=False, indent=4)
            logger.info(f"Отчет успешно сохранен в {filename}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении отчета в {filename}: {str(e)}")

        return result

    return wrapper


def report_to_file_with_name(filename: str):
    """
    Декоратор, принимает параметр filename и возвращает декоратор
    который записывает возвращаемое значение функции в указанный файл.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            kwargs['filename'] = filename
            return report_to_file(func)(*args, **kwargs)

        return wrapper

    return decorator


@report_to_file
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает данные о расходах для указанной категории за последние три месяца
    начиная с указанной даты (или текущей даты, если она не указана).

    Args:
        транзакции: DataFrame, содержащие данные о транзакциях
        категория: Категория для анализа
        дата: Дата ссылки (формат: ГГГГ-ММ-ДД) или None для текущей даты.

    Returns:
        DataFrame с данными о расходах для категории за последние 3 месяца
    """
    try:
        # Преобразует date string в datetime, если она указана, в противном случае использует текущую дату
        if date is None:
            ref_date = datetime.now()
        else:
            ref_date = datetime.strptime(date, "%Y-%m-%d")

        # Рассчитывает диапазон дат (последние 3 месяца)
        start_date = ref_date - timedelta(days=90)

        # Проверяет, что 'Дата операции' - это datetime
        transactions['Дата операции'] = pd.to_datetime(
            transactions['Дата операции'],
            format='%d.%m.%Y %H:%M:%S',
            dayfirst=True
        )

        # Фильтрует транзакции по категории и диапазону дат
        filtered = transactions[
            (transactions['Категория'] == category) &
            (transactions['Дата операции'] >= start_date) &
            (transactions['Дата операции'] <= ref_date) &
            (transactions['Сумма операции'] < 0)
            ].copy()

        if filtered.empty:
            logger.warning(f"No transactions found for category '{category}' in the specified period")
            return pd.DataFrame(columns=['Месяц', 'Сумма'])

        # Переводит суммы расходов в положительные значения
        filtered['Сумма операции'] = filtered['Сумма операции'].abs()

        # Группирует по месяцам и суммирует расходы
        result = filtered.groupby(
            pd.Grouper(key='Дата операции', freq='ME')  # Using 'ME' instead of deprecated 'M'
        )['Сумма операции'].sum().reset_index()

        # Форматирование дат
        result['Дата операции'] = result['Дата операции'].dt.strftime('%Y-%m')
        result.columns = ['Месяц', 'Сумма']

        return result

    except Exception as e:
        logger.error(f"Ошибка в spending_by_category: {str(e)}")
        return pd.DataFrame(columns=['Месяц', 'Сумма'])
