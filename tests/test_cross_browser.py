import pytest
import allure
from selenium import webdriver
from pages.home_page import HomePage




def get_driver(browser):
    if browser == 'chrome':
        return webdriver.Chrome()
    elif browser == 'firefox':
        return webdriver.Firefox()
    elif browser == 'safari':
        return webdriver.Safari()
    elif browser == 'edge':
        return webdriver.Edge()
    else:
        raise ValueError(f"Unsupported browser: {browser}")


@allure.title("Кросс-браузерная проверка отображения кнопки 'Log in'")
@allure.description("Проверка, что кнопка входа отображается в разных браузерах")
@pytest.mark.parametrize('browser', ['chrome', 'firefox', 'safari', 'edge'])
def test_site_functionality(browser):
    with allure.step(f"Инициализация драйвера для браузера: {browser}"):
        driver = get_driver(browser)
    try:
        with allure.step("Открыть сайт"):
            driver.get(BASE_URL)
            home_page = HomePage(driver)
        with allure.step("Проверить, что кнопка 'Log in' отображается"):
            assert home_page.is_log_in_button_displayed(), (
                f"Кнопка 'Log in' не отображается в браузере {browser}"
            )
    finally:
        with allure.step(f"Закрытие браузера: {browser}"):
            driver.quit()
