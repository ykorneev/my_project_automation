import pytest
import time
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
    """Фикстура инициализирует WebDriver и открывает сайт"""
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()


# 1. Замер времени загрузки главной страницы
def test_page_load(driver):
    home_page = HomePage(driver)
    start_time = time.time()
    driver.get(BASE_URL)
    assert home_page.is_page_loaded(), "Главная страница не загрузилась!"
    load_time = time.time() - start_time
    print(f'Время загрузки главной страницы: {load_time:.2f} секунд')
    assert load_time < 5, f"Страница загружается слишком долго: {load_time:.2f} секунд"


def test_page_product_load(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    product_name = "Samsung galaxy s6"
    start_time = time.time()
    home_page.open_product(product_name)
    assert product_page.is_product_page_loaded(product_name), "Страница товара не загрузилась!"
    load_time = time.time() - start_time
    print(f"Время загрузки страницы товара: {load_time:.2f} секунд")
    assert load_time < 5, f"Страница загружается слишком долго: {load_time:.2f} секунд"