import json
from unittest.mock import MagicMock, patch

from src.views import main_info


# Тест главной функции с мокированием всех зависимостей
def test_main_info():
    # Мокируем все функции, которые вызывает main_info
    with patch("src.views.get_time_for_greeting") as mock_greeting, \
            patch("src.views.get_data_time") as mock_data_time, \
            patch("src.views.get_path_and_period") as mock_get_path, \
            patch("src.views.get_card_with_spend") as mock_cards, \
            patch("src.views.get_top_transactions") as mock_top, \
            patch("src.views.get_currency") as mock_currency, \
            patch("src.views.get_stock") as mock_stock:
        # Настраиваем моки
        mock_greeting.return_value = "Добрый день"
        mock_data_time.return_value = ["01.01.2023", "15.01.2023"]
        mock_get_path.return_value = MagicMock()  # Мок DataFrame
        mock_cards.return_value = [{"last_digits": "1234", "total_spend": -100}]
        mock_top.return_value = [{"amount": "500", "category": "Еда"}]
        mock_currency.return_value = [{"currency": "USD", "rate": "75.5"}]
        mock_stock.return_value = [{"stock": "AAPL", "price": 150.5}]

        # Вызываем тестируемую функцию
        result = main_info("2023-01-15 12:00:00")
        data = json.loads(result)

        # Проверяем результаты
        assert data["greeting"] == "Добрый день"
        assert len(data["cards"]) == 1
        assert data["cards"][0]["last_digits"] == "1234"
        assert data["currency_rates"][0]["currency"] == "USD"
        assert data["stock_prices"][0]["stock"] == "AAPL"
