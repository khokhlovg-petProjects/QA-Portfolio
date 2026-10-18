import allure
import pytest

from config import BASE_URL, LOGIN_PASSWORD, LOGIN_USERNAME
from pages import InventoryPage, LoginPage


@pytest.fixture(scope="session")
def storage_state_path(browser):
    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(LOGIN_USERNAME, LOGIN_PASSWORD)
    # Кука появляется только после перехода, поэтому состояние сохраняем
    # не сразу после клика, иначе в файл запишется пустая сессия.
    page.wait_for_url(f"{BASE_URL}inventory.html")

    path = "state.json"
    context.storage_state(path=path)

    context.close()
    return path


@pytest.fixture
def authenticated_page(browser, storage_state_path):
    context = browser.new_context(storage_state=storage_state_path)
    page = context.new_page()
    page.goto(f"{BASE_URL}inventory.html")
    yield page
    context.close()


@pytest.fixture
def inventory_page(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(LOGIN_USERNAME, LOGIN_PASSWORD)
    return InventoryPage(page)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        hook_page = item.funcargs.get("page")
        if hook_page is not None:
            screenshot = hook_page.screenshot()
            allure.attach(
                screenshot,
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
