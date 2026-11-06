import allure
import pytest
from pages.gpb_api_client import GpbApiClient


@allure.epic("Автоматизация банковских сайтов")
@allure.feature("API Бэкенда Газпромбанка")
@pytest.mark.api
class TestGpbEmailPrediction:

    @pytest.fixture(autouse=True)
    def setup_api(self):
        self.api_client = GpbApiClient()

    @allure.story("Проверка подсказок ФИО с автоматической валидацией контракта")
    @pytest.mark.parametrize("query, parts, expected_key", [
        ("Халимов", "surname", "surname"),
        ("Роман", "name", "name"),
        ("Ильгизович", "second_name", "second_name")
    ])
    def test_fio_predictions_pom(self, query, parts, expected_key):

        response = self.api_client.get_fio_predictions(query=query, parts=parts)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"

        data = response.json()

        with allure.step(f"Бизнес-проверка содержимого для поля {parts} с запросом {query}"):
            assert len(data["items"]) > 0, f"Бэкенд вернул пустой список для ФИО: {query}"

            for item in data["items"]:
                assert query in item[expected_key] or item[expected_key] in query or query in item["value"], \
                    f"Подсказка не совпадает с поисковым запросом. Ожидалось совпадение с: {query}"

    @allure.story("Проверка подсказок Email с автоматической валидацией контракта")
    @pytest.mark.parametrize("search_query", ["3235", "3235@mail.ru"])
    def test_email_predictions_pom(self, search_query):

        response = self.api_client.get_email_predictions(query=search_query)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"

        data = response.json()

        with allure.step(f"Бизнес-проверка содержимого для email-запроса: {search_query}"):
            if "@" in search_query:
                assert len(data["items"]) > 0, f"Ожидались подсказки для email: {search_query}"
                for item in data["items"]:
                    base_prefix = search_query.split("@")[0]
                    assert base_prefix in item[
                        "value"], f"Подсказка '{item['value']}' не содержит префикс '{base_prefix}'"
            else:
                assert len(data["items"]) == 0, f"Ожидался пустой список для префикса без @"
