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

BASE_URL = "https://www.demoblaze.com/"


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()


# 1. Добавление одного товара в корзину
def test_add_one_item_to_cart(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    home_page.open_product("Samsung galaxy s6")
    product_page.add_to_cart()
    home_page.go_to_home()
    cart_page.open_cart()
    assert "Samsung galaxy s6" in cart_page.get_cart_items(), "Товар не добавлен в корзину"
    cart_page.delete_item()

# 2. Добавление нескольких товаров в корзину
def test_add_multiple_items_to_cart(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    # Добавление первого товара
    home_page.open_product("Samsung galaxy s6")
    product_page.add_to_cart()
    home_page.go_to_home()
    home_page.wait_for_products_to_load()
    home_page.open_product("Nokia lumia 1520")
    product_page.add_to_cart()
    cart_page.open_cart()
    cart_items = cart_page.get_cart_items()
    assert "Samsung galaxy s6" in cart_items, "Товар 'Samsung galaxy s6' не добавлен в корзину"
    assert "Nokia lumia 1520" in cart_items, "Товар 'Nokia lumia 1520' не добавлен в корзину"

# 3. Удаление товара из корзины
def test_delete_item_from_cart(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    home_page.open_product("Samsung galaxy s6")
    product_page.add_to_cart()
    cart_page.open_cart()
    cart_page.delete_item()
    assert "Samsung galaxy s6" in cart_page.get_cart_items(), "Товар удалился из корзины!"

# 4. Проверка оформления заказа
def test_order_placement(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    home_page.open_product("Nexus 6")
    product_page.add_to_cart()
    cart_page.open_cart()
    cart_page.checkout(
        name="TestUser",
        country="Poland",
        city="Warsaw",
        card="1234567890123456",
        month="12",
        year="2025"
    )
    assert cart_page.is_order_successful(), "Заказ не оформился"


# 5. Проверка авторизации
def test_login(driver):
    auth_page = AuthPage(driver)
    assert auth_page.login("TestYura123", "Test12345"), "Не удалось войти в систему!"

# 6. Проверка выхода из системы
def test_logout(driver):
    auth_page = AuthPage(driver)
    auth_page.login("TestYura123", "Test12345")
    assert auth_page.is_logged_in(), "Вход в систему не был выполнен!"
    auth_page.logout()
    try:
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located(auth_page.USER_WELCOME))
    except TimeoutException:
        pass  # Если элемент уже исчез, просто продолжаем
    assert not auth_page.check_if_logged_in(), "Выход не выполнен!"

# 7. Проверка отправки сообщения в Contact Us
def test_contact_us(driver):
    contact_page = ContactPage(driver)  # Теперь передаем driver
    contact_page.open_contact_form()
    contact_page.send_message("test@example.com", "Test User", "This is a test message.")
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert_text = alert.text
    assert "Thanks for the message!!" in alert_text, "Сообщение не отправлено"
    alert.accept()


# 8. Проверка загрузки главной страницы
def test_homepage(driver):
    home_page = HomePage(driver)
    assert home_page.is_logo_displayed(), "Логотип не отображается"


# 9. Проверка фильтрации товаров по категориям
def test_category_filter(driver):
    home_page = HomePage(driver)
    home_page.select_category("Laptops")
    products = home_page.get_product_names()
    assert len(products) > 0, "Товары не отображаются в категории Laptops"

# 10. Добавление товара в корзину (пользователь авторизован)
def test_add_to_cart(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    auth_page = AuthPage(driver)
    auth_page.login("TestYura123", "Test12345")
    home_page.select_category("Laptops")
    home_page.open_product("MacBook air")
    product_page.add_to_cart()
    cart_page.open_cart()
    cart_page.checkout(
        name="TestUser",
        country="Poland",
        city="Warsaw",
        card="1234567890123456",
        month="12",
        year="2025"
    )

    assert cart_page.is_order_successful(), "Заказ не оформился"
    cart_page.confirm_order()
    assert home_page.is_logo_displayed(), "Главная страница не загрузилась"


# 11. Оформление заказа с пустым полем номером карты
def test_incorrect_card_number(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    home_page.select_category("Laptops")
    home_page.open_product("MacBook air")
    product_page.add_to_cart()
    cart_page.open_cart()
    cart_page.checkout(
        name="Yura",
        country="Poland",
        city="Warsaw",
        card="1234567890123456",
        month="12",
        year="2025"
    )
    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        assert "Please fill out Name and Creditcard." in alert_text, f"Алерт не содержит ожидаемый текст: {alert_text}"
        alert.accept()
    except TimeoutException:
        pytest.fail("Алерт не появился! Возможно, валидация не работает.")

# 12. Оформление заказа с пустым полем Name
def test_empty_name(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    home_page.select_category("Laptops")
    home_page.open_product("MacBook air")
    product_page.add_to_cart()
    cart_page.open_cart()
    cart_page.checkout(
        name="",
        country="USA",
        city="New York",
        card="1234567890123456",
        month="12",
        year="2025"
    ) # Оформление заказа без имени
    alert_text = driver.switch_to.alert.text
    assert "Please fill out Name and Creditcard." in alert_text, f"Алерт не содержит ожидаемый текст: {alert_text}"
    driver.switch_to.alert.accept()

# 13. Оформление заказа с пустым полем Country
def test_empty_field_country(driver):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    home_page.select_category("Laptops")
    home_page.open_product("MacBook air")
    product_page.add_to_cart()
    cart_page.open_cart()
    cart_page.checkout(name="Yura", country="", city="Warsaw", card="123456789012", month="January", year="2001")
    assert cart_page.is_order_successful(), "Оформление заказа не прошло"
    cart_page.confirm_order()
    assert home_page.is_logo_displayed(), "Главная страница не загрузилась"


# 14. Фильтрация товаров
def test_phones_category(driver):
    home_page = HomePage(driver)
    home_page.select_category("Phones")
    product_names = home_page.get_product_names()
    expected_phones = {
        "Samsung galaxy s6", "Nokia lumia 1520", "Nexus 6",
        "Samsung galaxy s7", "Iphone 6 32gb", "Sony xperia z5",
        "HTC One M9"
    }
    assert set(product_names).issubset(
        expected_phones), f"Найден не телефон: {set(product_names) - expected_phones}"


def test_laptops_category(driver):
    home_page = HomePage(driver)
    home_page.select_category("Laptops")
    product_names = home_page.get_product_names()
    expected_laptops = {
        "Sony vaio i5", "Sony vaio i7", "MacBook air",
        "Dell i7 8gb", "MacBook Pro", "2017 Dell 15.6 Inch"
    }
    assert set(product_names).issubset(
        expected_laptops), f"Найден не ноутбук: {set(product_names) - expected_laptops}"


def test_monitors_category(driver):
    home_page = HomePage(driver)
    home_page.select_category("Monitors")
    product_names = home_page.get_product_names()
    expected_monitors = {"Apple monitor 24", "ASUS Full HD"}
    assert set(product_names).issubset(
        expected_monitors), f"Найден не монитор: {set(product_names) - expected_monitors}"
