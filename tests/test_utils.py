import json
from unittest.mock import Mock

from src.utils import get_currency, get_stock


# Тест для get_currency
def test_get_currency(monkeypatch, tmp_path):
    # 1. Подготовка тестовых данных
    test_settings = {"user_currencies": ["USD", "EUR"]}
    settings_file = tmp_path / "test_settings.json"
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(test_settings, f)

    # 2. Мокируем requests
    mock_responses = [
        {"query": {"from": "USD"}, "result": 75.5},
        {"query": {"from": "EUR"}, "result": 80.2}
    ]

    def mock_request(*args, **kwargs):
        mock = Mock()
        mock.json.return_value = mock_responses.pop(0)
        mock.status_code = 200
        return mock

    monkeypatch.setattr("requests.request", mock_request)

    # 3. Вызов тестируемой функции
    result = get_currency(str(settings_file))

    # 4. Проверки
    assert len(result) == 2
    assert {"currency": "USD", "rate": "75.5"} in result
    assert {"currency": "EUR", "rate": "80.2"} in result


# Тест для get_stock
def test_get_stock(monkeypatch, tmp_path):
    # 1. Подготовка тестовых данных
    test_settings = {"user_stocks": ["AAPL", "MSFT"]}
    settings_file = tmp_path / "test_stocks.json"
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(test_settings, f)

    # 2. Мокируем requests
    mock_response = {
        "data": [
            {"symbol": "AAPL", "close": 150.5},
            {"symbol": "MSFT", "close": 250.75}
        ]
    }

    def mock_get(*args, **kwargs):
        mock = Mock()
        mock.json.return_value = mock_response
        mock.status_code = 200
        mock.raise_for_status.return_value = None
        return mock

    monkeypatch.setattr("requests.get", mock_get)

    # 3. Вызов тестируемой функции
    result = get_stock(str(settings_file))

    # 4. Проверки
    assert len(result) == 2
    assert {"stock": "AAPL", "price": 150.5} in result
    assert {"stock": "MSFT", "price": 250.75} in result
