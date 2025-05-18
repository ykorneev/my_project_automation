import pytest
import allure
from pages.home_page import HomePage


@allure.title("Фильтрация товаров по категории 'Laptops'")
@allure.description("Проверка, что после выбора категории 'Laptops' отображаются соответствующие товары")
def test_filter_laptops(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    with allure.step("Выбрать категорию 'Laptops'"):
        home_page.select_category("Laptops")
    with allure.step("Получить список отображаемых товаров"):
        products = home_page.get_product_names()
    with allure.step("Проверить, что список товаров не пуст"):
        assert len(products) > 0, "Товары не отображаются в категории 'Laptops'"


@allure.title("Фильтрация товаров по категории 'Phones'")
@allure.description("Проверка, что после выбора категории 'Phones' отображаются соответствующие товары")
def test_filters_phones(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    with allure.step("Выбрать категорию 'Phones'"):
        home_page.select_category("Phones")
    with allure.step("Получить список отображаемых товаров"):
        products = home_page.get_product_names()
    with allure.step("Проверить, что список товаров не пуст"):
        assert len(products) > 0, "Товары не отображаются в категории 'Phones'"


@allure.title("Фильтрация товаров по категории 'Monitors'")
@allure.description("Проверка, что после выбора категории 'Monitors' отображаются товары из этой категории")
def test_filters_monitors(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    with allure.step("Выбрать категорию 'Monitors'"):
        home_page.select_category("Monitors")
    with allure.step("Получить список отображаемых товаров"):
        products = home_page.get_product_names()
    with allure.step("Проверить, что список товаров не пуст"):
        assert len(products) > 0, "Товары не отображаются в категории 'Monitors'"


@allure.title("Возврат на главную страницу по клику на логотип")
@allure.description("Проверка, что при клике на логотип происходит возврат на главную страницу и она загружается")
def test_back_to_the_home_page(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    with allure.step("Перейти в категорию 'Monitors'"):
        home_page.select_category("Monitors")
    with allure.step("Нажать на логотип сайта для возврата на главную"):
        home_page.click_logo()
    with allure.step("Проверить, что главная страница загружена"):
        assert home_page.is_logo_displayed(), "Главная страница не загрузилась после клика по логотипу"


@allure.title("Открытие карточки товара")
@allure.description("Проверка, что при клике на товар открывается его страница")
def test_open_product_card(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    with allure.step("Открыть карточку товара 'Samsung galaxy s6'"):
        home_page.open_product("Samsung galaxy s6")
    with allure.step("Проверить, что страница товара загружена"):
        assert home_page.is_product_page_loaded("Samsung galaxy s6"), "Страница товара не открылась"


@allure.title("Модальное окно 'About Us'")
@allure.description("Проверка открытия и закрытия модального окна 'About Us'")
def test_about_us_modal(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    with allure.step("Открыть модальное окно 'About Us'"):
        home_page.open_about_us()
    with allure.step("Проверить, что окно 'About Us' отображается"):
        assert home_page.is_about_us_displayed(), "Окно 'About Us' не появилось"
    with allure.step("Закрыть окно 'About Us'"):
        home_page.close_about_us()
    with allure.step("Проверить, что окно 'About Us' закрыто"):
        assert not home_page.is_about_us_displayed(), "Окно 'About Us' не закрылось"