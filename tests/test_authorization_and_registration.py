from common_imports import *


BASE_URL = "https://www.demoblaze.com/"

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

# 1. Проверка загрузки главной страницы
def test_homepage(driver):
    assert "STORE" in driver.title

# 2. Проверка отображения лого
def test_logo(driver):
    assert driver.find_element(By.ID, "nava").is_displayed()

# 3. Проверка отображения кнопки "Sign up"
def test_sign_up_button(driver):
    assert driver.find_element(By.ID, "signin2").is_displayed()

# 4. Проверка отображения кнопки "Log in"
def test_log_in_button(driver):
    assert driver.find_element(By.ID, "login2").is_displayed()

# 5. Регистрация нового пользователя
def test_registration_form(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.ID, "signin2").click()
    wait.until(EC.element_to_be_clickable((By.ID, "sign-username"))).send_keys("TestYura123")
    driver.find_element(By.ID, "sign-password").send_keys("Test12345")
    driver.find_element(By.XPATH, "//button[text()='Sign up']").click()
    alert = wait.until(EC.alert_is_present())
    assert "This user already exist." in alert.text
    alert.accept()

# 6. Вход в систему
def test_login(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.ID, "login2").click()
    wait.until(EC.element_to_be_clickable((By.ID, "loginusername"))).send_keys("TestYura123")
    driver.find_element(By.ID, "loginpassword").send_keys("Test12345")
    driver.find_element(By.XPATH, "//button[text()='Log in']").click()
    assert wait.until(EC.text_to_be_present_in_element((By.ID, "nameofuser"), "Welcome TestYura123"))

# 7. Выход из системы
def test_login_logout_flow(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.ID, "login2").click()
    wait.until(EC.element_to_be_clickable((By.ID, "loginusername"))).send_keys("TestYura123")
    driver.find_element(By.ID, "loginpassword").send_keys("Test12345")
    driver.find_element(By.XPATH, "//button[text()='Log in']").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "nameofuser"), "Welcome TestYura123"))
    driver.find_element(By.ID, "logout2").click()
    wait.until(EC.element_to_be_clickable((By.ID, "login2")))
    assert driver.find_element(By.CLASS_NAME, "carousel-inner").is_displayed()

# 8. Вход с неверным паролем
def test_invalid_password(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.ID, "login2").click()
    wait.until(EC.element_to_be_clickable((By.ID, "loginusername"))).send_keys("TestYura123")
    wait.until(EC.element_to_be_clickable((By.ID, "loginpassword"))).send_keys("WrongPassword")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in']"))).click()
    alert = wait.until(EC.alert_is_present())
    assert "Wrong password" in alert.text, f"Expected alert text to contain 'Wrong password', but got {alert.text}"
    alert.accept()

# 9. Вход с неверным логином
def test_invalid_username(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.ID, "login2").click()
    wait.until(EC.element_to_be_clickable((By.ID, "loginusername"))).send_keys("NoLogin")
    wait.until(EC.element_to_be_clickable((By.ID, "loginpassword"))).send_keys("Test12345")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in']"))).click()
    alert = wait.until(EC.alert_is_present())
    assert "User does not exist" in alert.text, f"Expected alert text to contain 'User does not exist', but got {alert.text}"
    alert.accept()

# 10. Регистрация уже существующего пользователя
def test_registration_existing_user(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.ID, "signin2").click()
    wait.until(EC.element_to_be_clickable((By.ID, "sign-username"))).send_keys("TestYura123")
    wait.until(EC.element_to_be_clickable((By.ID, "sign-password"))).send_keys("Test12345")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign up']"))).click()
    alert = wait.until(EC.alert_is_present())
    assert "This user already exist." in alert.text, f"Expected alert text to contain 'Sign up', but got {alert.text}"
    alert.accept()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#signInModal > div > div > div.modal-footer > button.btn.btn-secondary"))).click()
    assert driver.find_element(By.LINK_TEXT, "Samsung galaxy s6").is_displayed() is True



