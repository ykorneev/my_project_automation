import pytest
from pages.home_page import HomePage
from pages.contact_page import ContactPage

@pytest.fixture(scope="module")
def driver():
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("https://www.demoblaze.com/")
    yield driver
    driver.quit()

# 1. Фильтр по категории Laptops
def test_filter_laptops(driver):
    home_page = HomePage(driver)
    home_page.filter_by_category("Laptops")
    assert home_page.is_category_loaded(), "Категория Laptops не загрузилась!"

# 2. Фильтр по категории Phones
def test_filter_phones(driver):
    home_page = HomePage(driver)
    home_page.filter_by_category("Phones")
    assert home_page.is_category_loaded(), "Категория Phones не загрузилась!"

# 3. Фильтр по категории Monitors
def test_filter_monitors(driver):
    home_page = HomePage(driver)
    home_page.filter_by_category("Monitors")
    assert home_page.is_category_loaded(), "Категория Monitors не загрузилась!"

# 4. Возвращение на главную страницу
def test_back_to_home_page(driver):
    home_page = HomePage(driver)
    home_page.filter_by_category("Monitors")
    home_page.go_to_home()
    assert home_page.is_logo_displayed(), "Главная страница не загрузилась!"

# 5. Открытие карточки товара
def test_open_product_card(driver):
    home_page = HomePage(driver)
    home_page.open_product("Samsung galaxy s6")
    assert home_page.is_product_page_loaded("Samsung galaxy s6"), "Страница товара не открылась!"

# 6. Переход на вкладку "About Us"
def test_about_us_modal(driver):
    home_page = HomePage(driver)
    home_page.open_about_us()
    assert home_page.is_about_us_displayed(), "Окно 'About Us' не появилось!"
    home_page.close_about_us()
    assert not home_page.is_about_us_displayed(), "Окно 'About Us' не закрылось!"

# 7. Переход на страницу "Contact"
def test_contact_us(driver):
    contact_page = ContactPage(driver)
    contact_page.open_contact_form()
    contact_page.fill_contact_form("test_test@test.com", "Yura Korneev", "Test Message")
    assert contact_page.is_contact_form_sent(), "Сообщение не отправлено!"