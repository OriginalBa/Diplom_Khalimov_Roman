from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class GpbMainPage(BasePage):
    URL = "https://gazprombank.ru"

    PREMIUM_MENU_LINK = (By.XPATH,
                         "//p[text()='Премиум'] | //p[contains(@class, 'MenuTilesItem') and text()='Премиум']")

    PREMIUM_MOBILE_LINK = (By.XPATH, (
        "//a[@href='/premium/'] | "
        "//a[contains(@data-metric-element-id, 'Премиум')] | "
        "//a[contains(@class, 'MenuTilesItem') and .//p[text()='Премиум']]"
    ))

    def open(self):
        print(f"Открываем главную страницу Газпромбанка: {self.URL}")
        self.open_url(self.URL)
        self.clean_popups_if_exists()

    def click_premium(self):
        window_width = self.driver.get_window_size()['width']

        if window_width < 1012:
            print(f"[MOBILE UI] Ширина {window_width}px. Кликаем по точной ссылке из верстки через JS...")

            try:

                element = self.driver.find_element(*self.PREMIUM_MOBILE_LINK)
            except Exception:

                element = self.driver.find_element(*self.PREMIUM_MENU_LINK)

            self.driver.execute_script("arguments[0].click();", element)
        else:
            print(f"[DESKTOP UI] Стандартный клик по плитке меню 'Премиум'...")
            self.click_element(self.PREMIUM_MENU_LINK)
