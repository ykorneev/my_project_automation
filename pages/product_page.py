from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductPage(BasePage):
    ADD_TO_CART = (By.LINK_TEXT, "Add to cart")
    PRODUCT_TITLE = (By.TAG_NAME, "h2")

    def add_to_cart(self):
        self.click(self.ADD_TO_CART)
        self.accept_alert()

    def is_product_page_loaded(self, expected_name):
        product_title = self.wait.until(EC.visibility_of_element_located(self.PRODUCT_TITLE))
        return product_title.text.strip() == expected_name