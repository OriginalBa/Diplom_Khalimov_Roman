from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class GpbMainPage(BasePage):
    URL = "https://gazprombank.ru"

    PREMIUM_MENU_LINK = (By.XPATH,
                         "//p[text()='Премиум'] | //p[contains(@class, 'MenuTilesItem') and text()='Премиум']")

    def open(self):
        print(f"Открываем главную страницу Газпромбанка: {self.URL}")
        self.open_url(self.URL)

        self.clean_popups_if_exists()

    def click_premium(self):
        print("Кликаем по плитке меню 'Премиум'...")
        self.click_element(self.PREMIUM_MENU_LINK)
