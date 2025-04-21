import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import AuthPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.contact_page import ContactPage

BASE_URL = "https://www.demoblaze.com/"

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()

# 1. Проверка загрузки главной страницы
def test_homepage(driver):
    home_page = HomePage(driver)
    assert home_page.is_logo_displayed(), "Главная страница не загрузилась"

# 2. Проверка отображения кнопки "Sign up"
def test_sign_up_button(driver):
    home_page = HomePage(driver)
    assert home_page.is_sign_up_button_displayed(), "Кнопка 'Sign up' не отображается"

# 3. Проверка отображения кнопки "Log in"
def test_log_in_button(driver):
    auth_page = AuthPage(driver)
    assert auth_page.is_log_in_button_displayed(), "Кнопка 'Log in' не отображается"

# 4.
def test_login(driver):
    auth_page = AuthPage(driver)
    auth_page.open_login_form()
    auth_page.enter_credentials(username="TestYura123", password="Test12345")
    auth_page.submit_login()
    assert auth_page.is_logged_in(), "Вход в систему не выполнен"


# 5. Выход из системы
def test_login_logout_flow(driver):
    auth_page = AuthPage(driver)
    auth_page.login("TestYura123", "Test12345")
    auth_page.logout()
    assert auth_page.is_logged_out(), "Выход из системы не выполнен"

# 6. Вход с неверным паролем
def test_invalid_password(driver):
    auth_page = AuthPage(driver)
    auth_page.login("TestYura123", "WrongPassword")
    assert auth_page.is_login_failed(), "Ожидалось предупреждение о неверном пароле"

# 7. Вход с неверным логином
def test_invalid_username(driver):
    auth_page = AuthPage(driver)
    auth_page.login("NoLogin", "Test12345")
    assert auth_page.is_invalid_username_alert_present(), "Ожидалось предупреждение о неверном логине"

# 10. Регистрация уже существующего пользователя
def test_registration_existing_user(driver):
    auth_page = AuthPage(driver)
    auth_page.register("TestYura123", "Test12345")
    assert auth_page.is_existing_user_alert_present(), "Ожидалось предупреждение о существующем пользователе"
