import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def clean_popups_if_exists(self):
        """Метод для автоматического закрытия всплывающих окон Газпромбанка"""
        print("Проверяем наличие всплывающих окон и куки...")

        cookie_btn_locator = (By.XPATH, (
            "//button[@title='Закрыть'] | "
            "//*[contains(text(), 'Хорошо') or contains(text(), 'Принять') or contains(text(), 'ОК')]"
        ))

        advert_close_locator = (By.XPATH,
                                "//button[./svg] | //*[contains(@class, 'close') or contains(@class, 'Close')]")

        # Закрываем куки
        try:
            cookie_btn = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable(cookie_btn_locator))

            self.driver.execute_script("arguments[0].click();", cookie_btn)
            print("[ПОП-АП] Окно Cookie/Баннер успешно закрыто.")
        except TimeoutException:
            print("[ПОП-АП] Первое окно не появилось, проверяем следующее...")

        # Закрываем дополнительную рекламу
        try:
            advert_close = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(advert_close_locator))

            self.driver.execute_script("arguments[0].click();", advert_close)
            print("[ПОП-АП] Дополнительный рекламный баннер успешно закрыт.")
        except TimeoutException:
            print("[ПОП-АП] Дополнительных баннеров не обнаружено.")

    def click_element(self, locator, timeout=10):
        """Безопасный клик по элементу с ожиданием"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        try:
            element.click()
        except Exception:

            self.driver.execute_script("arguments[0].click();", element)

    def get_element_text(self, locator, timeout=15):
        """Получение текста из элемента"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text
