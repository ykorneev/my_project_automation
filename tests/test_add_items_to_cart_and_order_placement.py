import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.auth_page import AuthPage
from pages.contact_page import ContactPage



# 1. Добавление одного товара в корзину
@allure.title("Добавление одного товара в корзину")
@allure.description("Проверка добавления товара 'Samsung galaxy s6' в корзину")
def test_add_one_item_to_cart(driver, base_url):
    driver.get(BASE_URL)
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
@allure.title("Добавление нескольких товаров в корзину")
@allure.description("Проверка добавления двух товаров: 'Samsung galaxy s6' и 'Nokia lumia 1520' в корзину")
def test_add_multiple_items_to_cart(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    with allure.step("Добавление 'Samsung galaxy s6' в корзину"):
        home_page.open_product("Samsung galaxy s6")
        product_page.add_to_cart()
        home_page.go_to_home()
        home_page.wait_for_products_to_load()

    with allure.step("Добавление 'Nokia lumia 1520' в корзину"):
        home_page.open_product("Nokia lumia 1520")
        product_page.add_to_cart()

    with allure.step("Переход в корзину и проверка содержимого"):
        cart_page.open_cart()
        cart_items = cart_page.get_cart_items()

        assert "Samsung galaxy s6" in cart_items, \
            "Товар 'Samsung galaxy s6' не найден в корзине"
        assert "Nokia lumia 1520" in cart_items, \
            "Товар 'Nokia lumia 1520' не найден в корзине"

# 3. Удаление товара из корзины
@allure.title("Удаление товара из корзины")
@allure.description("Проверка удаления товара из корзины")
def test_delete_item_from_cart(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    home_page.open_product("Samsung galaxy s6")
    product_page.add_to_cart()
    cart_page.open_cart()
    cart_page.delete_item()
    assert "Samsung galaxy s6" in cart_page.get_cart_items(), "Товар удалился из корзины!"

# 4. Проверка оформления заказа
@allure.title("Оформление заказа")
@allure.description("Проверка успешного оформления заказа с корректными данными")
def test_order_placement(driver, base_url):
    driver.get(BASE_URL)
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
@allure.title("Авторизация")
@allure.description("Проверка входа в систему с валидными учетными данными")
def test_login(driver, base_url):
    driver.get(BASE_URL)
    auth_page = AuthPage(driver)
    assert auth_page.login("TestYura123", "Test12345"), "Не удалось войти в систему!"

# 6. Проверка выхода из системы
@allure.title("Выход из системы")
@allure.description("Проверка выхода из учетной записи после авторизации")
def test_logout(driver, base_url):
    driver.get(BASE_URL)
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
@allure.title("Отправка сообщения через форму Contact Us")
@allure.description("Проверка, что сообщение успешно отправляется через форму 'Contact Us'")
def test_contact_us(driver, base_url):
    driver.get(BASE_URL)
    contact_page = ContactPage(driver)

    with allure.step("Открыть форму обратной связи"):
        contact_page.open_contact_form()

    with allure.step("Заполнить форму и отправить сообщение"):
        contact_page.send_message(
            email="test@example.com",
            name="Test User",
            message="This is a test message."
        )

    with allure.step("Проверить появление алерта и его текст"):
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert_text = alert.text
            assert alert_text.strip() == "Thanks for the message!!", \
                f"Алерт содержит неверный текст: '{alert_text}'"
            alert.accept()
        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(), name="no_alert", attachment_type=allure.attachment_type.PNG)
            assert False, "Алерт не появился — сообщение не было отправлено"


# 8. Проверка загрузки главной страницы
@allure.title("Загрузка главной страницы")
@allure.description("Проверка отображения логотипа как подтверждение загрузки главной страницы")
def test_homepage(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)

    with allure.step("Проверить отображение логотипа на главной странице"):
        assert home_page.is_logo_displayed(), "Логотип не отображается — главная страница не загрузилась"


# 9. Проверка фильтрации товаров по категориям
@allure.title("Фильтрация товаров по категории 'Laptops'")
@allure.description("Проверка, что при выборе категории 'Laptops' отображаются соответствующие товары")
def test_category_filter(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)

    with allure.step("Выбрать категорию 'Laptops'"):
        home_page.select_category("Laptops")

    with allure.step("Получить список названий товаров из категории"):
        products = home_page.get_product_names()

    with allure.step("Проверить, что список товаров не пустой"):
        assert len(products) > 0, "Товары не отображаются в категории 'Laptops'"

# 10. Добавление товара в корзину (пользователь авторизован)
@allure.title("Добавление товара в корзину авторизованным пользователем и оформление заказа")
@allure.description("Проверка успешного добавления 'MacBook air' в корзину и оформления заказа после авторизации")
def test_add_to_cart(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    auth_page = AuthPage(driver)

    with allure.step("Авторизация пользователя"):
        assert auth_page.login("TestYura123", "Test12345"), "Не удалось авторизоваться"

    with allure.step("Выбор категории 'Laptops' и открытие товара 'MacBook air'"):
        home_page.select_category("Laptops")
        home_page.open_product("MacBook air")

    with allure.step("Добавление товара в корзину"):
        product_page.add_to_cart()

    with allure.step("Оформление заказа"):
        cart_page.open_cart()
        cart_page.checkout(
            name="TestUser",
            country="Poland",
            city="Warsaw",
            card="1234567890123456",
            month="12",
            year="2025"
        )

    with allure.step("Проверка успешного оформления заказа"):
        assert cart_page.is_order_successful(), "Заказ не оформился"

    with allure.step("Подтверждение заказа и возврат на главную"):
        cart_page.confirm_order()
        assert home_page.is_logo_displayed(), "Главная страница не загрузилась после оформления заказа"


# 11. Оформление заказа с пустым полем номером карты
@allure.title("Оформление заказа с пустым полем карты")
@allure.description("Проверка, что при попытке оформить заказ без номера карты появляется предупреждение")
def test_incorrect_card_number(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    with allure.step("Открытие товара 'MacBook air' и добавление в корзину"):
        home_page.select_category("Laptops")
        home_page.open_product("MacBook air")
        product_page.add_to_cart()

    with allure.step("Попытка оформить заказ с пустым номером карты"):
        cart_page.open_cart()
        cart_page.checkout(
            name="Yura",
            country="Poland",
            city="Warsaw",
            card="",  # ПУСТОЕ поле карты
            month="12",
            year="2025"
        )

    with allure.step("Проверка появления алерта с сообщением об ошибке"):
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert_text = alert.text.strip()
            assert alert_text == "Please fill out Name and Creditcard.", \
                f"Алерт содержит неожиданный текст: '{alert_text}'"
            alert.accept()
        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(), name="no_alert", attachment_type=allure.attachment_type.PNG)
            pytest.fail("Алерт не появился — возможно, валидация не сработала")

# 12. Оформление заказа с пустым полем Name
@allure.title("Оформление заказа с пустым полем имени")
@allure.description("Проверка, что при оформлении заказа без имени появляется соответствующий алерт")
def test_empty_name(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    with allure.step("Открытие товара 'MacBook air' и добавление в корзину"):
        home_page.select_category("Laptops")
        home_page.open_product("MacBook air")
        product_page.add_to_cart()

    with allure.step("Попытка оформить заказ без указания имени"):
        cart_page.open_cart()
        cart_page.checkout(
            name="",  # Пустое имя
            country="USA",
            city="New York",
            card="1234567890123456",
            month="12",
            year="2025"
        )

    with allure.step("Проверка появления алерта с ошибкой валидации"):
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert_text = alert.text.strip()
            assert alert_text == "Please fill out Name and Creditcard.", \
                f"Алерт содержит неожиданный текст: '{alert_text}'"
            alert.accept()
        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(), name="no_alert_name", attachment_type=allure.attachment_type.PNG)
            pytest.fail("Алерт не появился — возможно, валидация поля Name не работает")

# 13. Оформление заказа с пустым полем Country
@allure.title("Оформление заказа с пустым полем 'Country'")
@allure.description("Проверка, что заказ оформляется даже при отсутствии страны")
def test_empty_field_country(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    with allure.step("Выбор товара 'MacBook air' и добавление в корзину"):
        home_page.select_category("Laptops")
        home_page.open_product("MacBook air")
        product_page.add_to_cart()

    with allure.step("Оформление заказа с пустым полем Country"):
        cart_page.open_cart()
        cart_page.checkout(
            name="Yura",
            country="",  # Пустая страна
            city="Warsaw",
            card="123456789012",
            month="January",
            year="2001"
        )

    with allure.step("Проверка успешного оформления заказа"):
        assert cart_page.is_order_successful(), "Оформление заказа не прошло"

    with allure.step("Подтверждение заказа и возврат на главную"):
        cart_page.confirm_order()
        assert home_page.is_logo_displayed(), "Главная страница не загрузилась после заказа"


# 14. Фильтрация товаров
@allure.title("Фильтрация товаров по категории 'Phones'")
@allure.description("Проверка, что при выборе категории 'Phones' отображаются только соответствующие товары")
def test_phones_category(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)

    with allure.step("Выбрать категорию 'Phones'"):
        home_page.select_category("Phones")

    with allure.step("Получить названия всех отображаемых товаров"):
        product_names = home_page.get_product_names()

    expected_phones = {
        "Samsung galaxy s6", "Nokia lumia 1520", "Nexus 6",
        "Samsung galaxy s7", "Iphone 6 32gb", "Sony xperia z5",
        "HTC One M9"
    }

    with allure.step("Проверить, что все товары соответствуют категории 'Phones'"):
        unexpected_items = set(product_names) - expected_phones
        assert not unexpected_items, f"Найдены товары, не относящиеся к категории 'Phones': {unexpected_items}"


@allure.title("Фильтрация товаров по категории 'Laptops'")
@allure.description("Проверка, что отображаются только ноутбуки при выборе категории 'Laptops'")
def test_laptops_category(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)

    with allure.step("Выбрать категорию 'Laptops'"):
        home_page.select_category("Laptops")

    with allure.step("Получить список отображаемых товаров"):
        product_names = home_page.get_product_names()

    expected_laptops = {
        "Sony vaio i5", "Sony vaio i7", "MacBook air",
        "Dell i7 8gb", "MacBook Pro", "2017 Dell 15.6 Inch"
    }

    with allure.step("Проверить, что отображаются только ноутбуки"):
        unexpected_items = set(product_names) - expected_laptops
        assert not unexpected_items, \
            f"Найдены товары, не относящиеся к категории 'Laptops': {unexpected_items}"


@allure.title("Фильтрация товаров по категории 'Monitors'")
@allure.description("Проверка, что при выборе категории 'Monitors' отображаются только мониторы")
def test_monitors_category(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)

    with allure.step("Выбрать категорию 'Monitors'"):
        home_page.select_category("Monitors")

    with allure.step("Получить список отображаемых товаров"):
        product_names = home_page.get_product_names()

    expected_monitors = {"Apple monitor 24", "ASUS Full HD"}

    with allure.step("Проверить, что отображаются только мониторы"):
        unexpected_items = set(product_names) - expected_monitors
        assert not unexpected_items, \
            f"Найдены товары, не относящиеся к категории 'Monitors': {unexpected_items}"
