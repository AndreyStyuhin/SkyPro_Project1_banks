import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    # Создаем директорию для логов, если ее нет
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)

    # Основной логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Формат сообщений
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Консольный вывод
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Файловый вывод (с ротацией)
    file_handler = RotatingFileHandler(
        filename=logs_dir / 'app.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Логирование необработанных исключений
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.critical(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception
