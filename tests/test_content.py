import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.auth_page import AuthPage
from pages.contact_page import ContactPage

BASE_URL = "https://www.demoblaze.com/"

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

# 1. Тест на проверку отображения картинок товаров
def test_product_images(driver):
    home_page = HomePage(driver)
    assert home_page.are_product_images_displayed(), "Товары не найдены или у некоторых отсутствуют изображения!"

# 2. Тест на проверку отображения цен товаров
def test_product_prices(driver):
    home_page = HomePage(driver)
    assert home_page.are_product_prices_displayed(), "Некоторые товары не имеют цены!"

# 3. Кнопка Next
def test_next_button(driver):
    home_page = HomePage(driver)
    home_page.click_next_button()
    assert home_page.are_products_updated_after_next(), "По нажатию кнопки Next товары не обновились"