from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class HomePage(BasePage):
    LOGO = (By.ID, "nava")
    PRODUCTS_SECTION = (By.ID, "tbodyid")
    SIGN_UP_BUTTON = (By.ID, "signin2")
    LOGIN_BUTTON = (By.ID, "login2")
    CATEGORY_LINK = (By.LINK_TEXT, "{category}")
    PRODUCT_LINK = (By.LINK_TEXT, "{product_name}")
    PRODUCT_TITLE = (By.TAG_NAME, "h2")
    ABOUT_US_BUTTON = (By.XPATH, "//a[text()='About us']")  # Кнопка "About Us"
    ABOUT_US_MODAL = (By.XPATH, "//div[@id='videoModal' and contains(@class, 'show')]")  # Модальное окно
    CLOSE_ABOUT_US_BUTTON = (By.XPATH, "//div[@id='videoModal']//button[text()='Close']")  # Кнопка закрытия
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".card img")
    PRODUCT_PRICES = (By.TAG_NAME, "h5")
    NEXT_BUTTON = (By.ID, "next2")
    PRODUCT_CONTAINER = (By.CLASS_NAME, "col-lg-9")
    PRODUCT_SPECIFIC_LINK = (By.LINK_TEXT, "Samsung galaxy s6")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def filter_by_category(self, category_name):
        category_locator = (By.LINK_TEXT, category_name)
        self.wait.until(EC.element_to_be_clickable(category_locator)).click()
        self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title")))

    def is_category_loaded(self):
        return len(self.driver.find_elements(By.CLASS_NAME, "card-title")) > 0

    def go_to_home(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGO)).click()

    def is_logo_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.LOGO)).is_displayed()

    def open_product(self, product_name):
        product_locator = (By.LINK_TEXT, product_name)
        self.wait.until(EC.element_to_be_clickable(product_locator)).click()

    def is_product_page_loaded(self, expected_name):
        product_title = self.wait.until(EC.visibility_of_element_located(self.PRODUCT_TITLE))
        return product_title.text.strip().lower() == expected_name.lower()

    def open_about_us(self):
        self.wait.until(EC.element_to_be_clickable(self.ABOUT_US_BUTTON)).click()

    def is_about_us_displayed(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ABOUT_US_MODAL)).is_displayed()
        except:
            return False

    def close_about_us(self):
        self.wait.until(EC.element_to_be_clickable(self.CLOSE_ABOUT_US_BUTTON)).click()
        self.wait.until(EC.invisibility_of_element_located(self.ABOUT_US_MODAL))

    def are_product_images_displayed(self):
        images = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_IMAGES))
        return all(img.get_attribute("src") for img in images)

    def are_product_prices_displayed(self):
        prices = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_PRICES))
        for price in prices:
            price_text = price.text.strip()
            if not price_text or not any(char.isdigit() for char in price_text):
                print(f"Товар без цены найден: {price_text}")
                return False
        return True

    def click_next_button(self):
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

    def are_products_updated_after_next(self):
        return len(self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_CONTAINER))) > 0

    def is_log_in_button_displayed(self):
        return self.wait.until(EC.presence_of_element_located(self.LOGIN_BUTTON)).is_displayed()

    def is_page_loaded(self):
        return self.wait.until(EC.presence_of_element_located(self.LOGIN_BUTTON)).is_displayed()

    def open_product(self, product_name):
        product_link_locator = (By.LINK_TEXT, product_name)
        product_link = self.wait.until(EC.element_to_be_clickable(product_link_locator))
        product_link.click()

    def wait_for_products_to_load(self):
        self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title")))

    def select_category(self, category_name):
        category_locator = (By.LINK_TEXT, category_name)
        self.wait.until(EC.element_to_be_clickable(category_locator)).click()

    def get_product_names(self):
        product_elements = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title")))
        return [product.text.strip() for product in product_elements]

    def is_sign_up_button_displayed(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.SIGN_UP_BUTTON)).is_displayed()
        except TimeoutException:
            return False