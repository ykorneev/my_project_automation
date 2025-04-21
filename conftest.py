import pytest
from selenium import webdriver
import allure

BASE_URL = "https://www.demoblaze.com/"

@pytest.fixture(scope="function")  # Запуск браузера перед каждым тестом
def driver():
    driver = webdriver.Chrome()  # Открытие браузера
    driver.get(BASE_URL)  # Переход на главную страницу
    yield driver
    driver.quit()  # Закрытие браузера после каждого теста