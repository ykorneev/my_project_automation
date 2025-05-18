import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://www.demoblaze.com/"

def get_driver(browser):
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
        return webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--no-remote")
        profile_path = tempfile.mkdtemp()
        options.profile = profile_path
        return webdriver.Firefox(options=options)

    raise NotImplementedError(f"{browser} is not supported in CI environment")


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser", default="chrome")
    driver = get_driver(browser)
    driver.get(BASE_URL)
    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to run tests (chrome or firefox)"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.allure_report_dir = "allure-results"