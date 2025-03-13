from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, UnexpectedAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AuthPage(BasePage):
    LOGIN_BUTTON = (By.ID, "login2")
    USERNAME_FIELD = (By.ID, "sign-username")
    PASSWORD_FIELD = (By.ID, "sign-password")
    LOGIN_USERNAME_FIELD = (By.ID, "loginusername")
    LOGIN_PASSWORD_FIELD = (By.ID, "loginpassword")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Log in']")
    USER_WELCOME = (By.ID, "nameofuser")
    LOGOUT_BUTTON = (By.ID, "logout2")
    SIGN_UP_BUTTON = (By.ID, "signin2")
    CONFIRM_SIGN_UP_BUTTON = (By.XPATH, "//button[text()='Sign up']")
    SIGN_UP_ALERT = (By.CLASS_NAME, "modal-content")
    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//button[text()='Log in']")

    def login(self, username, password):
        self.click(self.LOGIN_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_USERNAME_FIELD))
        username_field = self.wait.until(EC.presence_of_element_located(self.LOGIN_USERNAME_FIELD))
        username_field.clear()
        username_field.send_keys(username)
        password_field = self.wait.until(EC.presence_of_element_located(self.LOGIN_PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(password)
        self.click(self.SUBMIT_BUTTON)
        try:
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert_text = alert.text
            print(f"⚠ Обнаружен алерт: {alert_text}")
            alert.accept()
            return False
        except:
            pass
        return self.is_logged_in()

    def is_logged_in(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.USER_WELCOME))
            return "Welcome" in element.text
        except TimeoutException:
            return False

    def logout(self):
        self.click(self.LOGOUT_BUTTON)
        try:
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(self.USER_WELCOME))
        except TimeoutException:
            pass
        return not self.is_logged_in()
    def is_log_in_button_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.LOGIN_BUTTON)).is_displayed()

    def register(self, username, password):

        self.click(self.SIGN_UP_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD))
        self.wait.until(EC.element_to_be_clickable(self.USERNAME_FIELD)).send_keys(username)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(password)
        self.click(self.CONFIRM_SIGN_UP_BUTTON)

    def is_registration_successful(self):
            alert = self.wait.until(EC.alert_is_present())
            success_text = "This user already exist."
            is_successful = success_text in alert.text
            alert.accept()
            return is_successful

    def open_login_form(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()

    def enter_credentials(self, username, password):
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_USERNAME_FIELD)).send_keys(username)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_PASSWORD_FIELD)).send_keys(password)

    def submit_login(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON)).click()

    def is_logged_out(self):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.USER_WELCOME)
            )
        except TimeoutException:
            return False

    def is_invalid_password_alert_present(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body"), "Wrong password")
            )
            return True
        except TimeoutException:
            print("Сообщение об ошибке не найдено в HTML страницы!")
            return False

    def is_invalid_username_alert_present(self):
        try:
            alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert_text = alert.text
            print(f"Найденный текст алерта: {alert_text}")
            return "This user already exist." in alert_text
        except TimeoutException:
            print("Алерт о существующем пользователе не появился!")
            return False

    def is_existing_user_alert_present(self):
        try:
            alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert_text = alert.text
            print(f"Найденный текст алерта: {alert_text}")
            return "This user already exist." in alert_text
        except TimeoutException:
            print("Алерт о существующем пользователе не появился!")
            return False

    def is_login_failed(self):
        try:
            return WebDriverWait(self.driver, 5).until(
             EC.presence_of_element_located(self.LOGIN_BUTTON)
            ).is_displayed()
        except TimeoutException:
            return False

    def check_if_logged_in(self):
        try:
            return self.driver.find_element(*self.USER_WELCOME).is_displayed()
        except:
            return False

    def get_product_names(self):
        product_elements = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title")))
        return [product.text.strip() for product in product_elements]