import pytest
import allure
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

# 1. Проверка загрузки главной страницы
@allure.title("Проверка загрузки главной страницы")
@allure.description("Убедиться, что при открытии сайта отображается логотип, подтверждающий загрузку страницы")
def test_homepage(driver):
    home_page = HomePage(driver)
    with allure.step("Проверить наличие логотипа на главной странице"):
        assert home_page.is_logo_displayed(), "Главная страница не загрузилась — логотип не найден"

# 2. Проверка отображения кнопки "Sign up"
@allure.title("Проверка отображения кнопки 'Sign up'")
@allure.description("Убедиться, что на главной странице отображается кнопка регистрации 'Sign up'")
def test_sign_up_button(driver):
    home_page = HomePage(driver)
    with allure.step("Проверить, что кнопка 'Sign up' отображается на странице"):
        assert home_page.is_sign_up_button_displayed(), "Кнопка 'Sign up' не отображается на главной странице"

# 3. Проверка отображения кнопки "Log in"
@allure.title("Проверка отображения кнопки 'Log in'")
@allure.description("Убедиться, что кнопка входа в систему 'Log in' доступна на странице")
def test_log_in_button(driver):
    auth_page = AuthPage(driver)
    with allure.step("Проверить, что кнопка 'Log in' отображается"):
        assert auth_page.is_log_in_button_displayed(), "Кнопка 'Log in' не отображается на странице"

# 4.
@allure.title("Проверка входа в систему")
@allure.description("Авторизация пользователя с корректными учетными данными и проверка успешного входа")
def test_login(driver):
    auth_page = AuthPage(driver)
    with allure.step("Открыть форму входа"):
        auth_page.open_login_form()
    with allure.step("Ввести логин и пароль"):
        auth_page.enter_credentials(username="TestYura123", password="Test12345")
    with allure.step("Отправить форму входа"):
        auth_page.submit_login()
    with allure.step("Проверить, что пользователь успешно авторизован"):
        if not auth_page.is_logged_in():
            # Добавим скриншот и сообщение, если вход не удался
            allure.attach(driver.get_screenshot_as_png(), name="login_failed", attachment_type=allure.attachment_type.PNG)
            raise AssertionError("Вход в систему не выполнен")


# 5. Выход из системы
@allure.title("Проверка выхода из системы")
@allure.description("Авторизация пользователя и проверка корректного завершения сессии через выход")
def test_login_logout_flow(driver):
    auth_page = AuthPage(driver)
    with allure.step("Авторизоваться с валидными данными"):
        assert auth_page.login("TestYura123", "Test12345"), "Авторизация не выполнена"
    with allure.step("Выполнить выход из системы"):
        auth_page.logout()
    with allure.step("Проверить, что пользователь вышел из системы"):
        assert auth_page.is_logged_out(), "Выход из системы не выполнен"

# 6. Вход с неверным паролем
@allure.title("Проверка входа с неверным паролем")
@allure.description("Убедиться, что при вводе некорректного пароля появляется предупреждение и вход не выполняется")
def test_invalid_password(driver):
    auth_page = AuthPage(driver)
    with allure.step("Попытка входа с неверным паролем"):
        auth_page.login("TestYura123", "WrongPassword")
    with allure.step("Проверка, что вход не выполнен и отображается сообщение об ошибке"):
        assert auth_page.is_login_failed(), "Ожидалось предупреждение о неверном пароле"

# 7. Вход с неверным логином
@allure.title("Проверка входа с неверным логином")
@allure.description("Убедиться, что при вводе несуществующего логина появляется предупреждение об ошибке")
def test_invalid_username(driver):
    auth_page = AuthPage(driver)
    with allure.step("Попытка входа с несуществующим логином"):
        auth_page.login("NoLogin", "Test12345")
    with allure.step("Проверка появления предупреждения о неверном логине"):
        assert auth_page.is_invalid_username_alert_present(), "Ожидалось предупреждение о неверном логине"

# 10. Регистрация уже существующего пользователя
@allure.title("Регистрация с уже существующим логином")
@allure.description("Проверка, что при попытке регистрации с существующим именем пользователя появляется соответствующее предупреждение")
def test_registration_existing_user(driver):
    auth_page = AuthPage(driver)
    with allure.step("Попытка регистрации с уже существующим именем пользователя"):
        auth_page.register("TestYura123", "Test12345")
    with allure.step("Проверка появления предупреждения о существующем пользователе"):
        assert auth_page.is_existing_user_alert_present(), \
            "Ожидалось предупреждение о существующем пользователе"
