import time

from common_imports import *


BASE_URL = "https://www.demoblaze.com/"

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

# 1. Добавление одного товара в корзину
def test_add_one_item_to_cart(driver):
    wait = WebDriverWait(driver, 15)                                                                            # Ожидание до 10 секунд
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Samsung galaxy s6"))).click()                                 # Клик по товару "Samsung galaxy s6"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()                                       # Клик по кнопке "Add to cart"
    wait.until(EC.alert_is_present())
    driver.switch_to.alert.accept()                                                                                     # Ожидание и принятие alert-окна
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()                                              # Переход в корзину
    order_description = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/div/div[1]")))        # Проверка, что блок с описанием заказа отображается
    assert order_description.is_displayed()

# 2. Добавление нескольких товаров в корзину
def test_add_multiple_items_to_cart(driver):
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Samsung galaxy s6"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()                                       # Добавление первого товара

    WebDriverWait(driver, 15).until(EC.alert_is_present()).accept()

    wait.until(EC.element_to_be_clickable((By.ID, "nava"))).click()                                                     # Возврат на главную страницу

    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div/div[2]/div/div/h4/a"))).click()  # Добавление второго товара
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()
    WebDriverWait(driver, 15).until(EC.alert_is_present()).accept()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()                                              # Переход в корзину

    assert wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/div/div[1]"))).is_displayed()      # Проверка отображения описания заказа

# 3. Удаление товара из корзины
def test_delete_item_from_cart(driver):
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Samsung galaxy s6"))).click()                                 # Добавление первого товара
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()

    WebDriverWait(driver, 15).until(EC.alert_is_present()).accept()

    wait.until(EC.element_to_be_clickable((By.ID, "nava"))).click()                                                     # Возврат на главную страницу
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div[2]/div/div[2]/div/div/h4/a"))).click()  # Добавление второго товара
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()

    WebDriverWait(driver, 15).until(EC.alert_is_present()).accept()

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()                                              # Переход в корзину
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div[1]/div/table/tbody/tr[2]/td[4]/a"))).click()    # Удаление товара из корзины

    assert wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/div/div[1]"))).is_displayed()      # Проверка, что корзина отображается (можно также проверить отсутствие элемента)

# 4. Проверка добавления выбранного товара
def test_add_correct_item_to_cart(driver):
    wait = WebDriverWait(driver, 15)

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Samsung galaxy s6"))).click()                                 # Открываем страницу товара
    name_product = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h2"))).text
    price_product = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text.split(" ")[0]                # Получаем название и цену товара
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()                                       # Добавляем товар в корзину

    WebDriverWait(driver, 15).until(EC.alert_is_present()).accept()

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()                                              # Переходим в корзину
    cart_name_product = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[2]"))).text
    cart_price_product = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[3]"))).text                       # Получаем название и цену товара в корзине

    assert name_product == cart_name_product, f"Ожидалось {name_product}, но в корзине {cart_name_product}"
    assert price_product == cart_price_product, f"Ожидалось {price_product}, но в корзине {cart_price_product}"         # Проверка названия и цены
    cart_items = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[@class='success']")))                  # Проверка, что в корзине только один товар
    assert len(cart_items) == 1, f"Ожидался 1 товар в корзине, но найдено {len(cart_items)}"

# 5. Добавление товара в корзину (пользователь авторизован)
def test_add_to_cart(driver):
    wait = WebDriverWait(driver, 15)

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Laptops"))).click()                                           # Открытие категории "Laptops"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "MacBook air"))).click()                                       # Выбор "MacBook air"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()                                       # Добавление товара в корзину

    alert = wait.until(EC.alert_is_present())
    assert "Product added" in alert.text, f"Алерт не содержит ожидаемый текст: {alert.text}"
    alert.accept()

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()                                              # Переход в корзину

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#page-wrapper > div > div.col-lg-1 > button"))).click()    # Оформление заказа
    wait.until(EC.visibility_of_element_located((By.ID, "name"))).send_keys("Yura")                                     # Заполнение формы заказа
    driver.find_element(By.ID, "country").send_keys("Poland")
    driver.find_element(By.ID, "city").send_keys("Warsaw")
    driver.find_element(By.ID, "card").send_keys("1234567891011")
    driver.find_element(By.ID, "month").send_keys("January")
    driver.find_element(By.ID, "year").send_keys("2001")

    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))).click()            # Подтверждение заказа

    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Thank you for your purchase!"))    # Проверка успешного оформления заказа
    assert "Thank you for your purchase!" in driver.page_source, "Сообщение о покупке не найдено!"

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"))).click()   # Закрытие подтверждения заказа
    assert wait.until(EC.visibility_of_element_located((By.ID, "nava"))).is_displayed(), "Главная страница не загрузилась!"  # Проверка возврата на главную страницу


# 7. Оформление заказа с пустыми полями
def test_order_placement_with_empty_fields(driver):
    wait = WebDriverWait(driver, 15)                                                                            # Открытие категории "Laptops"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Laptops"))).click()                                           # Выбор "MacBook air"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "MacBook air"))).click()                                       # Добавление товара в корзину
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()
                                                                                                                        # Ожидание алерта и его подтверждение
    alert = wait.until(EC.alert_is_present())
    assert "Product added" in alert.text, f"Алерт не содержит ожидаемый текст: {alert.text}"
    alert.accept()
                                                                                                                        # Переход в корзину
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()                                              # Открытие формы заказа
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#page-wrapper > div > div.col-lg-1 > button"))).click()    # Подтверждение заказа без заполнения полей
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))).click()            # Ожидание алерта с ошибкой
    alert = wait.until(EC.alert_is_present())
    assert "Please fill out Name and Creditcard." in alert.text, f"Алерт не содержит ожидаемый текст: {alert.text}"
    alert.accept()

# 8. Оформление заказа с пустым полем номером карты
def test_incorrect_card_number(driver):
    wait = WebDriverWait(driver, 15)
                                                                                                                        # Открытие категории "Laptops"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Laptops"))).click()                                           # Выбор "MacBook air"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "MacBook air"))).click()                                       # Добавление товара в корзину
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()

    alert = wait.until(EC.alert_is_present())
    assert "Product added" in alert.text, f"Алерт не содержит ожидаемый текст: {alert.text}"
    alert.accept()
                                                                                                                        # Переход в корзину
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()                                              # Открытие формы заказа
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#page-wrapper > div > div.col-lg-1 > button"))).click()
                                                                                                                        # Заполнение формы заказа без номера карты
    wait.until(EC.visibility_of_element_located((By.ID, "name"))).send_keys("Yura")
    driver.find_element(By.ID, "country").send_keys("Poland")
    driver.find_element(By.ID, "city").send_keys("Warsaw")
    driver.find_element(By.ID, "card").send_keys("")  # Пустое поле номера карты
    driver.find_element(By.ID, "month").send_keys("January")
    driver.find_element(By.ID, "year").send_keys("2001")

    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))).click()            # Подтверждение заказа

    alert = wait.until(EC.alert_is_present())
    assert "Please fill out Name and Creditcard." in alert.text, f"Алерт не содержит ожидаемый текст: {alert.text}"
    alert.accept()


# 9. Пустое поле "Name"
def test_empty_name(driver):
    wait = WebDriverWait(driver, 15)
# Открытие категории "Laptops"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Laptops"))).click()
# Выбор "MacBook air"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "MacBook air"))).click()
# Добавление товара в корзину
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()

    alert = wait.until(EC.alert_is_present())
    assert "Product added" in alert.text, f"Алерт не содержит ожидаемый текст: {alert.text}"
    alert.accept()
# Переход в корзину
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()
# Открытие формы заказа
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#page-wrapper > div > div.col-lg-1 > button"))).click()
# Заполнение формы без имени
    wait.until(EC.visibility_of_element_located((By.ID, "name"))).send_keys("")
    driver.find_element(By.ID, "country").send_keys("Poland")
    driver.find_element(By.ID, "city").send_keys("Warsaw")
    driver.find_element(By.ID, "card").send_keys("123456789012")
    driver.find_element(By.ID, "month").send_keys("January")
    driver.find_element(By.ID, "year").send_keys("2001")
# Подтверждение заказа
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))).click()
# Ожидание алерта с ошибкой
    alert = wait.until(EC.alert_is_present())
    assert "Please fill out Name and Creditcard." in alert.text, f"Алерт не содержит ожидаемый текст: {alert.text}"
    alert.accept()

# 10. Пустое поле "Country"
def test_empty_field_country(driver):
    wait = WebDriverWait(driver, 15)
# Открытие категории "Laptops"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Laptops"))).click()
# Выбор "MacBook air"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "MacBook air"))).click()
# Добавление товара в корзину
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()
# Ожидание алерта и подтверждение
    alert = wait.until(EC.alert_is_present())
    assert "Product added" in alert.text, f"Алерт не содержит ожидаемый текст: {alert.text}"
    alert.accept()
# Переход в корзину
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()
# Открытие формы заказа
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#page-wrapper > div > div.col-lg-1 > button"))).click()
# Заполнение формы без страны
    wait.until(EC.visibility_of_element_located((By.ID, "name"))).send_keys("Yura")
    driver.find_element(By.ID, "country").send_keys("")
    driver.find_element(By.ID, "city").send_keys("Warsaw")
    driver.find_element(By.ID, "card").send_keys("123456789012")
    driver.find_element(By.ID, "month").send_keys("January")
    driver.find_element(By.ID, "year").send_keys("2001")
# Подтверждение заказа
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))).click()
# Проверка отображения окна подтверждения заказа
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Thank you for your purchase!"))
# Закрытие окна подтверждения
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"))).click()
# Проверка возврата на главную страницу
    assert wait.until(EC.visibility_of_element_located((By.ID, "nava"))).is_displayed()

# 11. Проверка, что после покупки корзина пуста
def test_cart_is_empty_after_purchase(driver):
    wait = WebDriverWait(driver, 15)
# Выбор товара
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Samsung galaxy s6"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))).click()
# Ожидание алерта и его подтверждение
    alert = wait.until(EC.alert_is_present())
    assert "Product added" in alert.text, f"Алерт не содержит ожидаемый текст: {alert.text}"
    alert.accept()
# Переход в корзину
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()
# Оформление заказа
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#page-wrapper > div > div.col-lg-1 > button"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "name"))).send_keys("Yura")
    driver.find_element(By.ID, "country").send_keys("")
    driver.find_element(By.ID, "city").send_keys("Warsaw")
    driver.find_element(By.ID, "card").send_keys("123456789012")
    driver.find_element(By.ID, "month").send_keys("January")
    driver.find_element(By.ID, "year").send_keys("2001")
 # Подтверждение заказа
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))).click()
# Проверка подтверждения заказа
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Thank you for your purchase!"))
# Закрытие окна подтверждения
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                           "body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > div > button"))).click()
# Проверка возврата на главную страницу
    assert wait.until(EC.visibility_of_element_located((By.ID, "nava"))).is_displayed()
# Проверка, что корзина пуста
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()
    assert not driver.find_elements(By.XPATH, "//tr[@class='success']"), "Корзина не пуста!"


# 12. Фильтрация товаров
def get_product_names(driver):
    # Получаем список товаров в текущей категории
    wait = WebDriverWait(driver, 15)
    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title")))
    return [product.text for product in products]


# Проверка, что в категории "Phones" только телефоны
def test_phones_category(driver):
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Phones"))).click()

    product_names = get_product_names(driver)

    expected_phones = [
        "Samsung galaxy s6", "Nokia lumia 1520", "Nexus 6",
        "Samsung galaxy s7", "Iphone 6 32gb", "Sony xperia z5",
        "HTC One M9"
    ]

    assert set(product_names).issubset(
        set(expected_phones)), f"Найден не телефон: {set(product_names) - set(expected_phones)}"


# Проверка, что в категории "Laptops" только ноутбуки
def test_laptops_category(driver):
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Laptops"))).click()

    product_names = get_product_names(driver)

    expected_laptops = [
        "Sony vaio i5", "Sony vaio i7", "MacBook air",
        "Dell i7 8gb", "MacBook Pro", "2017 Dell 15.6 Inch"
    ]

    assert set(product_names).issubset(
        set(expected_laptops)), f"Найден не ноутбук: {set(product_names) - set(expected_laptops)}"


# Проверка, что в категории "Monitors" только мониторы
def test_monitors_category(driver):
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Monitors"))).click()

    product_names = get_product_names(driver)

    expected_monitors = ["Apple monitor 24", "ASUS Full HD"]

    assert set(product_names).issubset(
        set(expected_monitors)), f"Найден не монитор: {set(product_names) - set(expected_monitors)}"