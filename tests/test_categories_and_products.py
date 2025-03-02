from common_imports import *

BASE_URL = "https://www.demoblaze.com/"

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

# 1. Фильтр по категории Laptops
def test_filter_laptops(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.LINK_TEXT, "Laptops").click()
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title")))
    assert len(driver.find_elements(By.CLASS_NAME, "card-title")) > 0

# 2. Фильтр по категории Phones
def test_filters_phones(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.LINK_TEXT, "Phones").click()
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title")))
    assert len(driver.find_elements(By.CLASS_NAME, "card-title")) > 0

# 3. Фильтр по категории Monitors
def test_filters_monitors(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.LINK_TEXT, "Monitors").click()
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title")))
    assert len(driver.find_elements(By.CLASS_NAME, "card-title")) > 0


# 4. Возвращение на главную страницу
def test_back_to_the_home_page(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.LINK_TEXT, "Monitors").click()
    wait.until(EC.element_to_be_clickable((By.ID, "nava"))).click()
    assert driver.find_element(By.ID, "nava").is_displayed()

# 5. Открытие карточки товара
def test_open_card_products(driver):
    wait = WebDriverWait(driver, 10)
    # Дожидаемся появления списка товаров перед кликом
    wait.until(EC.presence_of_element_located((By.ID, 'tbodyid')))
    product_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Samsung galaxy s6")))
    product_link.click()
    product_name = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h2")))

    # Проверяем, что название товара на странице соответствует ожидаемому
    assert product_name.text.strip() == "Samsung galaxy s6", f"Ожидалось 'Samsung galaxy s6', но найдено '{product_name.text.strip()}'"

# 6. Переход на вкладку "About Us"
def test_about_us_page(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.XPATH, "/html/body/nav/div[1]/ul/li[3]/a").click()
    modal_window = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div")))
    assert modal_window.is_displayed(), "Модальное окно 'About Us' появилось!"
    close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[3]/button")))
    close_button.click()
    wait.until(EC.invisibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div")))
    assert not modal_window.is_displayed(), "Модальное окно не закрылось!"


# 7. Переход на страницу "Contact"
def test_contact_us_page(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.XPATH, "/html/body/nav/div[1]/ul/li[2]/a").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control:nth-of-type(1)")))

    driver.find_element(By.CSS_SELECTOR, "input.form-control:nth-of-type(1)").send_keys("test_test@test.com")
    driver.find_element(By.XPATH, "(//input[@class='form-control'])[2]").send_keys("Yura Korneev")
    driver.find_element(By.XPATH, "(//textarea[@class='form-control'])[1]").send_keys("Test Message")

    send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[3]/button[2]")))
    send_button.click()

    alert = wait.until(EC.alert_is_present())
    assert "Thanks for the message!!" in alert.text
    alert.accept()








