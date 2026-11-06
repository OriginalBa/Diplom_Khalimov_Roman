import allure
import requests
from jsonschema import validate
from pages.gpb_api_schemas import FIO_JSON_SCHEMA, EMAIL_JSON_SCHEMA


class GpbApiClient:

    def __init__(self):
        self.base_url = "https://gazprombank.ru"
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Referer": "https://gazprombank.ru/premium",
                "Origin": "https://gazprombank.ru",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Priority": "u=1, i",
            }
        )

    def _send_request(self, method, method_url, **kwargs):
        url = f"{self.base_url}{method_url}"

        with allure.step(f"API Request: {method} {method_url}"):
            if "params" in kwargs and kwargs["params"]:
                allure.attach(
                    str(kwargs["params"]),
                    name="Query Params",
                    attachment_type=allure.attachment_type.TEXT,
                )
            if "json" in kwargs:
                allure.attach(
                    str(kwargs["json"]),
                    name="Request Body",
                    attachment_type=allure.attachment_type.JSON,
                )

            response = self.session.request(method, url, **kwargs)

            allure.attach(
                f"Status: {response.status_code}\nHeaders: {dict(response.headers)}",
                name="Response Info",
                attachment_type=allure.attachment_type.TEXT,
            )
            try:
                allure.attach(
                    response.text,
                    name="Response Body",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception:
                allure.attach(
                    response.text,
                    name="Response Body (Raw)",
                    attachment_type=allure.attachment_type.TEXT,
                )

            return response

    def get_email_predictions(self, query: str, ab_segment: str = "segment03"):

        method_url = "/api/v1/gazprombank/prediction/email/list/"
        params = {"ab_segment": ab_segment, "query": query}
        response = self._send_request("GET", method_url, params=params)

        with allure.step("Автоматическая валидация JSON-схемы Email"):
            validate(instance=response.json(), schema=EMAIL_JSON_SCHEMA)

        return response

    def get_fio_predictions(self, query: str, parts: str, ab_segment: str = "segment03"):

        method_url = "/api/v1/gazprombank/prediction/fio/list/"
        params = {
            "ab_segment": ab_segment,
            "query": query,
            "parts": parts
        }
        response = self._send_request("GET", method_url, params=params)

        with allure.step("Автоматическая валидация JSON-схемы ФИО"):
            validate(instance=response.json(), schema=FIO_JSON_SCHEMA)

        return response
