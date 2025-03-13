from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class ContactPage:
    CONTACT_BUTTON = (By.LINK_TEXT, "Contact")  # Кнопка открытия формы
    EMAIL_FIELD = (By.ID, "recipient-email")  # Поле для email (правильное имя)
    NAME_FIELD = (By.ID, "recipient-name")  # Поле для имени
    MESSAGE_FIELD = (By.ID, "message-text")  # Поле для сообщения
    SEND_BUTTON = (By.XPATH, "//button[text()='Send message']")  # Кнопка отправки


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_contact_form(self):
        self.wait.until(EC.element_to_be_clickable(self.CONTACT_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def fill_contact_form(self, email, name, message):
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)).send_keys(email)
        self.driver.find_element(*self.NAME_INPUT).send_keys(name)
        self.driver.find_element(*self.MESSAGE_INPUT).send_keys(message)
        self.wait.until(EC.element_to_be_clickable(self.SEND_BUTTON)).click()

    def is_contact_form_sent(self):
        alert = self.wait.until(EC.alert_is_present())
        result = "Thanks for the message!!" in alert.text
        alert.accept()
        return result

    def send_message(self, email, name, message):
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD)).send_keys(email)
        self.wait.until(EC.visibility_of_element_located(self.NAME_FIELD)).send_keys(name)
        self.wait.until(EC.visibility_of_element_located(self.MESSAGE_FIELD)).send_keys(message)
        self.wait.until(EC.element_to_be_clickable(self.SEND_BUTTON)).click()