import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class GpbPremiumPage(BasePage):
    URL = "https://www.gazprombank.ru/premium"

    PRIVILEGES_TAB = (By.CSS_SELECTOR, "button[title='Привилегии']")
    CONDITIONS_TAB = (By.CSS_SELECTOR, "button[title='Условия обслуживания']")
    DOCUMENTS_TAB = (By.CSS_SELECTOR, "button[title='Документы и тарифы']")

    HEADER_TEXT = (By.XPATH, "//*[contains(text(), 'Премиум') or contains(text(), 'Премиальный')]")
    ADVANTAGES_CARD = (By.XPATH, "//*[contains(text(), 'от 1 млн ₽')]")

    BONUS_INFO_TEXT = (By.XPATH, "//*[contains(text(), 'Газпром Бонус «Премиум»')]")
    PDF_DOCUMENT_LINK = (By.XPATH,
                         "//a[contains(@data-metric-element-id, 'Аэрофлот') or contains(@data-metric-element-id, 'Aeroflot')]")

    def open(self):
        print(f"Открываем страницу Премиума НАПРЯМУЮ: {self.URL}")
        self.open_url(self.URL)

        self.clean_popups_if_exists()

    def _click_tab_via_js(self, locator, tab_name):
        """Внутренний вспомогательный метод для безопасного переключения вкладок"""
        print(f"Ждем готовности интерфейса перед переходом на вкладку '{tab_name}'...")
        time.sleep(3)
        element = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(2)

    def click_privileges_tab(self):
        self._click_tab_via_js(self.PRIVILEGES_TAB, "Привилегии")

    def click_conditions_tab(self):
        self._click_tab_via_js(self.CONDITIONS_TAB, "Условия обслуживания")

    def click_documents_tab(self):
        self._click_tab_via_js(self.DOCUMENTS_TAB, "Документы и тарифы")

        print("Ожидаем подгрузку списка документов с сервера...")
        time.sleep(3)

    def get_header_text(self):
        return self.get_element_text(self.HEADER_TEXT)

    def get_all_card_text(self):
        return self.get_element_text(self.ADVANTAGES_CARD, timeout=15)

    def get_bonus_section_text(self):
        print("Собираем информацию о бонусной программе во вкладке Привилегии...")
        return self.get_element_text(self.BONUS_INFO_TEXT, timeout=15)

    def get_pdf_link_text(self):
        print("Ищем документ 'Аэрофлот Бонус' по атрибуту метрики...")
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.PDF_DOCUMENT_LINK)
        )

        return element.get_attribute("data-metric-element-id")
