import time
import allure
from pages.home_page import HomePage
from pages.product_page import ProductPage


# 1. Замер времени загрузки главной страницы
@allure.title("Замер времени загрузки главной страницы")
@allure.description("Проверка, что главная страница загружается менее чем за 5 секунд")
def test_page_load(driver, base_url):
    driver.get(BASE_URL)
    with allure.step("Начать замер времени и загрузить главную страницу"):
        start_time = time.time()
        driver.get("https://www.demoblaze.com/")
        load_time = time.time() - start_time
    with allure.step(f"Проверить, что страница загружается за {load_time:.2f} секунд"):
        allure.attach(str(load_time), name="Загрузка главной", attachment_type=allure.attachment_type.TEXT)
        assert load_time < 5, (
            f"Страница загружается слишком долго: {load_time:.2f} секунд")


# 2. Замер времени загрузки страницы товара
@allure.title("Замер времени загрузки страницы товара")
@allure.description("Проверка, что страница товара загружается менее чем за 5 секунд")
def test_page_product_load(driver, base_url):
    driver.get(BASE_URL)
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    product_name = "Samsung galaxy s6"
    with allure.step(f"Начать замер и открыть страницу товара '{product_name}'"):
        start_time = time.time()
        home_page.open_product(product_name)
        assert product_page.is_product_page_loaded(product_name), (
            "Страница товара не загрузилась!"
        )
        load_time = time.time() - start_time
    with allure.step(f"Проверить, что страница товара загружается за {load_time:.2f} секунд"):
        allure.attach(str(load_time), name="Загрузка товара", attachment_type=allure.attachment_type.TEXT)
        assert load_time < 5, (
            f"Страница товара загружается слишком долго: {load_time:.2f} секунд")
    load_time = time.time() - start_time
    print(f"Время загрузки страницы товара: {load_time:.2f} секунд")
    assert load_time < 5, (
        f"Страница загружается слишком долго: {load_time:.2f} секунд")