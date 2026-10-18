import allure
from pages.main_page import GpbMainPage
from pages.premium_page import GpbPremiumPage


@allure.epic("Автоматизация банковских сайтов")
@allure.feature("Навигация и парсинг условий")
class TestGpbPremium:

    @allure.story("Сквозной переход с главной страницы на Премиум")
    def test_navigate_to_gpb_premium(self, driver):
        main_page = GpbMainPage(driver)
        premium_page = GpbPremiumPage(driver)

        with allure.step("Открытие главной страницы"):
            main_page.open()
        with allure.step("Переход в раздел Премиум"):
            main_page.click_premium()
        with allure.step("Проверка заголовка премиальной страницы"):
            header = premium_page.get_header_text()
            assert "Премиум" in header or "Премиальный" in header

    @allure.story("Тест вкладки 'Условия обслуживания' — лимиты остатков")
    def test_collect_premium_tariffs_directly(self, driver):
        premium_page = GpbPremiumPage(driver)

        with allure.step("Прямое открытие страницы Премиум"):
            premium_page.open()
        with allure.step("Переход на вкладку 'Условия обслуживания'"):
            premium_page.click_conditions_tab()
        with allure.step("Сбор финансовых условий из карточки"):
            full_card_text = premium_page.get_all_card_text()
            allure.attach(full_card_text, name="Полные условия карточки")
            print(f"\n[УСПЕШНО СПАРСЕНО]:\n{full_card_text}\n")
            assert "1" in full_card_text

    @allure.story("Тест вкладки 'Привилегии' — бонусные программы")
    def test_check_privileges_tab(self, driver):
        premium_page = GpbPremiumPage(driver)

        with allure.step("Прямое открытие страницы Премиум"):
            premium_page.open()
        with allure.step("Переход на вкладку 'Привилегии'"):
            premium_page.click_privileges_tab()
        with allure.step("Сбор информации о бонусах Газпрома"):
            bonus_text = premium_page.get_bonus_section_text()
            allure.attach(bonus_text, name="Информация о Газпром Бонус")
            print(f"\n[УСПЕШНО СПАРСЕНО БОНУСЫ]:\n{bonus_text}\n")
            assert "Бонус" in bonus_text or "Премиум" in bonus_text

    @allure.story("Тест вкладки 'Документы и тарифы' — проверка документов сборника тарифов")
    def test_check_documents_tab(self, driver):
        premium_page = GpbPremiumPage(driver)

        with allure.step("Прямое открытие страницы Премиум"):
            premium_page.open()
        with allure.step("Переход на вкладку 'Документы и тарифы'"):
            premium_page.click_documents_tab()
        with allure.step("Поиск официальных документов тарифа"):
            doc_text = premium_page.get_pdf_link_text()
            allure.attach(doc_text, name="Текст найденного документа")
            print(f"\n[УСПЕШНО НАЙДЕН ДОКУМЕНТ]:\n{doc_text}\n")

            assert "Аэрофлот" in doc_text, f"Ожидался документ Аэрофлот Бонус, но найдено: {doc_text}"
