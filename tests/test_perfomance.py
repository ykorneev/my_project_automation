from common_imports import *


BASE_URL = "https://www.demoblaze.com/"

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()


import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.demoblaze.com/"


# 1. Замер времени загрузки главной страницы
def test_page_load(driver):
    start_time = time.time()
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login2")))
    end_time = time.time()

    load_time = end_time - start_time
    print(f'Время загрузки главной страницы: {load_time:.2f} секунд')

    assert load_time < 5, f"Страница загружается слишком долго: {load_time:.2f} секунд"


# 2. Замер времени загрузки страницы товара
def test_page_products(driver):
    wait = WebDriverWait(driver, 10)

    # Кликаем на товар и замеряем время загрузки страницы
    product_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Samsung galaxy s6")))
    start_time = time.time()
    product_link.click()

    wait.until(EC.presence_of_element_located((By.ID, "more-information")))  # Ожидание загрузки контента
    end_time = time.time()

    load_time = end_time - start_time
    print(f"Время загрузки страницы товара: {load_time:.2f} секунд")

    assert load_time < 5, f"Страница загружается слишком долго: {load_time:.2f} секунд"

