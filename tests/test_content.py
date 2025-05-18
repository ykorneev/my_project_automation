import pytest
import allure
from pages.home_page import HomePage



# 1. Проверка отображения изображений товаров
@allure.title("Проверка отображения изображений товаров")
@allure.description("Убедиться, что все отображаемые товары содержат изображения")
def test_product_images(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    with allure.step("Проверить, что у всех товаров есть изображения"):
        assert home_page.are_product_images_displayed(), (
            "Товары не найдены или у некоторых отсутствуют изображения")


# 2. Проверка отображения цен товаров
@allure.title("Проверка отображения цен товаров")
@allure.description("Убедиться, что у каждого товара на странице указана цена")
def test_product_prices(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    with allure.step("Проверить, что все товары содержат цену"):
        assert home_page.are_product_prices_displayed(), (
            "Некоторые товары не имеют цены")


# 3. Проверка работы кнопки 'Next'
@allure.title("Проверка работы кнопки 'Next'")
@allure.description("Убедиться, что при нажатии кнопки 'Next' происходит смена товаров")
def test_next_button(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    with allure.step("Нажать на кнопку 'Next'"):
        home_page.click_next_button()
    with allure.step("Проверить, что список товаров изменился"):
        assert home_page.are_products_updated_after_next(), (
            "По нажатию кнопки 'Next' товары не обновились")