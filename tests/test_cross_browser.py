from common_imports import *
from pages.home_page import HomePage  # Импортируем POM класс для главной страницы


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