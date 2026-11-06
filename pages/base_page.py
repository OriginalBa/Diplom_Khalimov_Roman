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
        print("Проверяем наличие всплывающих окон и куки (Desktop/Mobile)...")

        locators = [
            (By.XPATH, "//button[@title='Закрыть']"),
            (By.XPATH, "//button[contains(@class, 'ButtonClose_root')]"),
            (By.XPATH, "//*[contains(text(), 'Хорошо') or contains(text(), 'Принять') or contains(text(), 'ОК')]"),
            (By.XPATH, "//*[contains(@class, 'close') or contains(@class, 'Close')]")
        ]

        for locator in locators:
            try:

                element = WebDriverWait(self.driver, 1.5).until(EC.element_to_be_clickable(locator))

                self.driver.execute_script("arguments[0].click();", element)
                print(f"[ПОП-АП] Успешно закрыт элемент с локатором: {locator[1]}")
            except TimeoutException:

                continue

    def click_element(self, locator, timeout=10):

        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        try:
            element.click()
        except Exception:

            self.driver.execute_script("arguments[0].click();", element)

    def get_element_text(self, locator, timeout=15):

        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text
