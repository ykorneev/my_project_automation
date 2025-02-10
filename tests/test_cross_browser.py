from common_imports import *


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

@pytest.mark.parametrize('browser', ['chrome', 'firefox', 'safari', 'edge'])
def test_site_functionality(browser):
    driver = get_driver(browser)
    driver.get("https://www.demoblaze.com/")

    # Проверка, что на главной странице есть элемент, кнопка "Log in"
    assert driver.find_element(By.ID, "login2").is_displayed(), f"Сайт не работает в {browser}"


    driver.quit()