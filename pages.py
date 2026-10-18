import allure

from config import BASE_URL


class LoginPage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto(BASE_URL)

    @allure.step("Войти как {username}")
    def login(self, username: str, password: str):
        self.page.locator("#user-name").fill(username)
        self.page.locator("#password").fill(password)
        self.page.locator("#login-button").click()


class InventoryPage:
    def __init__(self, page):
        self.page = page

    def click_by_test_id(self, item_test_id: str):
        self.page.locator(f"[data-test='{item_test_id}']").click()

    @allure.step("Добавить товар в корзину")
    def add_item_to_cart(self, item_test_id: str):
        self.click_by_test_id(item_test_id)

    def get_cart_badge_count(self) -> int:
        # Пустую корзину saucedemo показывает отсутствием элемента, а не нулём в нём.
        badge = self.page.locator(".shopping_cart_badge")
        if badge.count() == 0:
            return 0
        return int(badge.inner_text())

    def go_into_cart(self, item_test_id: str):
        self.click_by_test_id(item_test_id)

    def delete_cart_element(self, item_test_id: str):
        self.click_by_test_id(item_test_id)

    def sort_custom_params(self, sort_value: str):
        self.page.locator("[data-test='product-sort-container']").select_option(value=sort_value)

    def check_all_prices(self) -> list[str]:
        return self.page.locator("[data-test='inventory-item-price']").all_inner_texts()


class BuyingProcess:
    def __init__(self, page):
        self.page = page

    def find_and_click_checkout_button(self):
        self.page.locator("[data-test='checkout']").click()

    def fill_out_address_form(self, first_name: str, second_name: str, zip_code: str):
        self.page.locator("[data-test='firstName']").fill(first_name)
        self.page.locator("[data-test='lastName']").fill(second_name)
        self.page.locator("[data-test='postalCode']").fill(zip_code)

    def continue_button_click(self):
        self.page.locator("[data-test='continue']").click()

    @allure.step("Завершить оформление заказа")
    def finish_button_click(self):
        self.page.locator("[data-test='finish']").click()

    def check_order_status(self) -> str:
        return self.page.locator("[data-test='complete-header']").inner_text()
