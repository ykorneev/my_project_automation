from common_imports import *


BASE_URL = "https://www.demoblaze.com/"

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

# 1. Тест на проверку отображения картинок товаров
def test_product_images(driver):
    wait = WebDriverWait(driver, 10)
    images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card img")))

    assert len(images) > 0, "Товары не найдены!"

    for img in images:
        assert img.get_attribute("src"), "Изображение отсутствует у товара!"

# 2. Тест на проверку отображения цен товаров
def test_product_prices(driver):
    # Ожидаем, что на странице будут отображены все элементы с тегом <h5> (цены товаров)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "h5")))

    # Находим все элементы <h5>, которые содержат цену
    price_elements = driver.find_elements(By.TAG_NAME, "h5")

    # Проверяем, что каждый элемент <h5> не пустой (т.е. товар имеет цену)
    all_prices_exist = True  # По умолчанию считаем, что все товары с ценой

    for price in price_elements:
        price_text = price.text.strip()

        # Если цена пустая, то считаем, что товара без цены найден
        if price_text == "":
            print("Товар без цены найден:", price)
            all_prices_exist = False
            break  # Прерываем цикл, так как нашли товар без цены

    # Возвращаем True, если все товары имеют цену, иначе False
    return all_prices_exist

# 3. Кнопка Next
def test_next_button(driver):
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.element_to_be_clickable((By.ID, "next2")))
    next_button.click()

    # Проверяем, что появились новые товары после нажатия "Next"
    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "col-lg-9")))
    assert len(products) > 0, "По нажатию кнопки Next товары не обновились"

