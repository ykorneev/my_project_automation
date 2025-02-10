import pytest
from selenium import webdriver
import allure

# Фикстура для запуска браузера
@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--headless")  # Открытие браузера в фоновом режиме
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

