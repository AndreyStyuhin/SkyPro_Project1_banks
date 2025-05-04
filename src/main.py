import logging

import pandas as pd

from logging_config import setup_logging
from src.reports import spending_by_category
from src.services import anylize_cashback
from src.views import main_info

# Инициализация логгера
setup_logging()
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting application")
    try:
        data_request = "2019-04-10 15:30:00"
        result_view = main_info(data_request)
        print(result_view)

        result_services = anylize_cashback("../data/operations.xlsx", 2018, 4)
        print(result_services)

        df = pd.read_excel("../data/operations.xlsx", sheet_name="Отчет по операциям")
        result_report = spending_by_category(df, "Ж/д билеты", "2019-04-10")
        print(result_report)

        logger.debug("Debug message")
        logger.info("Informational message")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
    finally:
        logger.info("Application finished")


if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     data_request = "2019-04-10 15:30:00"
#     result_view = main_info(data_request)
#     print(result_view)
#
#     result_services = anylize_cashback("../data/operations.xlsx", 2018, 4)
#     print(result_services)
#
#     df = pd.read_excel("../data/operations.xlsx", sheet_name="Отчет по операциям")
#     result_report = spending_by_category(df, "Ж/д билеты", "2019-04-10")
#     print(result_report)
