import pytest
from selenium import webdriver
import allure

@pytest.fixture(scope="function")  # Запуск браузера перед каждым тестом
def driver():
    driver = webdriver.Chrome()  # Открытие браузера
    driver.get("https://www.demoblaze.com/")  # Переход на главную страницу
    yield driver
    driver.quit()  # Закрытие браузера после каждого теста