import pytest
from selenium import webdriver
import allure

# Фикстура для запуска браузера
#@pytest.fixture(scope="session")
#def driver():
    #options = Options()
   # options.add_argument("--headless")  # Открытие браузера в фоновом режиме
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #yield driver
    #driver.quit()

@pytest.fixture(scope="function")  # Запуск браузера перед каждым тестом
def driver():
    driver = webdriver.Chrome()  # Открытие браузера
    driver.get("https://www.demoblaze.com/")  # Переход на главную страницу
    yield driver
    driver.quit()  # Закрытие браузера после каждого теста