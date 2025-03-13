from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class CartPage(BasePage):
    URL = "https://www.demoblaze.com/cart.html"
    CART_LINK = (By.LINK_TEXT, "Cart")
    CART_ITEMS = (By.XPATH, "//table[@class='table table-bordered table-hover table-striped']//tr/td[2]")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Place Order']")
    NAME_FIELD = (By.ID, "name")
    COUNTRY_FIELD = (By.ID, "country")
    CITY_FIELD = (By.ID, "city")
    CARD_FIELD = (By.ID, "card")
    MONTH_FIELD = (By.ID, "month")
    YEAR_FIELD = (By.ID, "year")
    PURCHASE_BUTTON = (By.XPATH, "//button[text()='Purchase']")
    CONFIRMATION_TEXT = (By.XPATH, "//h2[contains(text(),'Thank you for your purchase!')]")
    DELETE_BUTTON = (By.LINK_TEXT, "Delete")
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='OK']")

    def open_cart(self):
        self.click(self.CART_LINK)

    def get_cart_items(self):
        cart_items = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))
        return [item.text for item in cart_items]

    def checkout(self, name, country, city, card, month, year):
        self.click(self.PLACE_ORDER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.NAME_FIELD)).send_keys(name)
        self.wait.until(EC.visibility_of_element_located(self.COUNTRY_FIELD)).send_keys(country)
        self.wait.until(EC.visibility_of_element_located(self.CITY_FIELD)).send_keys(city)
        self.wait.until(EC.visibility_of_element_located(self.CARD_FIELD)).send_keys(card)
        self.wait.until(EC.visibility_of_element_located(self.MONTH_FIELD)).send_keys(month)
        self.wait.until(EC.visibility_of_element_located(self.YEAR_FIELD)).send_keys(year)
        self.click(self.PURCHASE_BUTTON)

    def is_order_successful(self):
        return bool(self.wait.until(EC.presence_of_element_located(self.CONFIRMATION_TEXT)))

    def delete_item(self):
        self.click(self.DELETE_BUTTON)

    def confirm_order(self):  # Новый метод
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON)).click()