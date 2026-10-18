import pytest

from config import BASE_URL
from pages import BuyingProcess, InventoryPage, LoginPage


def test_homepage_has_correct_title(page):
    page.goto(BASE_URL)
    assert page.title() == "Swag Labs"


def test_login_navigates_to_inventory_page(page, inventory_page):
    assert page.url == f"{BASE_URL}inventory.html"


def test_add_item_to_cart_updates_badge(authenticated_page):
    inventory = InventoryPage(authenticated_page)
    inventory.add_item_to_cart("add-to-cart-sauce-labs-backpack")
    assert inventory.get_cart_badge_count() == 1


@pytest.mark.parametrize(
    "username,password,expected_error_part",
    [
        ("locked_out_user", "secret_sauce", "locked out"),
        ("standard_user", "wrong_password", "do not match"),
        ("", "", "Username is required"),
    ],
)
def test_invalid_login_shows_error(page, username, password, expected_error_part):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(username, password)
    assert expected_error_part in page.locator("[data-test='error']").inner_text()


def test_remove_item_from_cart(inventory_page):
    inventory_page.add_item_to_cart("add-to-cart-sauce-labs-backpack")
    assert inventory_page.get_cart_badge_count() == 1

    inventory_page.go_into_cart("shopping-cart-link")
    inventory_page.delete_cart_element("remove-sauce-labs-backpack")
    assert inventory_page.get_cart_badge_count() == 0


def test_check_prices_with_sort(inventory_page):
    inventory_page.sort_custom_params("lohi")
    prices = [float(price.replace("$", "")) for price in inventory_page.check_all_prices()]
    assert prices == sorted(prices)


def test_full_checkout_flow(page, inventory_page):
    inventory_page.add_item_to_cart("add-to-cart-sauce-labs-backpack")
    inventory_page.go_into_cart("shopping-cart-link")

    buying_process = BuyingProcess(page)
    buying_process.find_and_click_checkout_button()
    buying_process.fill_out_address_form("Grigoriy", "Pobedonosniy", "111222")
    buying_process.continue_button_click()
    buying_process.finish_button_click()

    assert "Thank you for your order" in buying_process.check_order_status()
