from common_imports import *
from pages.home_page import HomePage

BASE_URL = "https://www.demoblaze.com/"

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

# 1. Тест на проверку отображения картинок товаров
def test_product_images(driver):
    home_page = HomePage(driver)
    assert home_page.are_product_images_displayed(), "Товары не найдены или у некоторых отсутствуют изображения!"

# 2. Тест на проверку отображения цен товаров
def test_product_prices(driver):
    home_page = HomePage(driver)
    assert home_page.are_product_prices_displayed(), "Некоторые товары не имеют цены!"

# 3. Кнопка Next
def test_next_button(driver):
    home_page = HomePage(driver)
    home_page.click_next_button()
    assert home_page.are_products_updated_after_next(), "По нажатию кнопки Next товары не обновились"