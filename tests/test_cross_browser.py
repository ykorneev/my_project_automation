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


# Функция для инициализации WebDriver в зависимости от браузера
def get_driver(browser):
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        return webdriver.Chrome(options=options)
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        return webdriver.Firefox(options=options)
    elif browser == 'safari':
        options = webdriver.SafariOptions()
        return webdriver.Safari(options=options)
    elif browser == 'edge':
        options = webdriver.EdgeOptions()
        return webdriver.Edge(options=options)
    else:
        raise ValueError(f"Браузер {browser} не поддерживается!")


@pytest.mark.parametrize('browser', ['chrome', 'firefox', 'safari', 'edge'])
def test_site_functionality(browser):
    driver = get_driver(browser)
    driver.get("https://www.demoblaze.com/")
    home_page = HomePage(driver)
    assert home_page.is_log_in_button_displayed(), f"Сайт не работает в {browser}!"
    driver.quit()