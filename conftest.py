import pytest
import allure
from pages import LoginPage, InventoryPage
from config import LOGIN_USERNAME, LOGIN_PASSWORD, BASE_URL

@pytest.fixture(scope="session")
def storage_state_path(browser):
    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(LOGIN_USERNAME, LOGIN_PASSWORD)

    path = "state.json"
    context.storage_state(path=path)

    context.close()
    return path

@pytest.fixture
def authenticated_page(browser, storage_state_path):
    context = browser.new_context(storage_state=storage_state_path)
    page = context.new_page()
    page.goto("https://www.saucedemo.com/inventory.html")
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
        # TODO: достань объект page из item.funcargs (это словарь всех фикстур текущего теста)
        # и, если он там есть, сделай screenshot и приложи его в Allure
        hookPage = item.funcargs.get("page") 
        if hookPage is not None:
            screenshot = hookPage.screenshot()
            allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
        pass
