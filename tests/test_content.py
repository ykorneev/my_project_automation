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
    wait = WebDriverWait(driver, 15)  # Увеличим timeout
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card")))

    prices = driver.find_elements(By.CSS_SELECTOR, ".card .price-container")

    assert len(prices) > 0, "Товары не найдены"

    for price in prices:
        price_text = price.text.strip()
        assert price_text.startswith("$"), f"Некорректная цена: {price_text}"

# 3. Кнопка Next
def test_next_button(driver):
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.element_to_be_clickable((By.ID, "next2")))
    next_button.click()

    # Проверяем, что появились новые товары после нажатия "Next"
    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "col-lg-9")))
    assert len(products) > 0, "По нажатию кнопки Next товары не обновились"

