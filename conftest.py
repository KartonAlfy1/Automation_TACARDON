import pytest
import json
from playwright.sync_api import sync_playwright, Playwright
from datetime import datetime
import os
import io
import logging
from pytest_html import extras

# option to run tests in headed or headless mode
def pytest_addoption(parser):
    # currently set to true headed
    parser.addoption("--headed", action="store_true", default=True, help="run tests in headed / headless mode")
    parser.addoption("--browser", action="store", default="chromium", choices=["chromium", "firefox", "webkit"],
                     help="Specify the browser to run tests on")

# provides the Playwright instance for the test session
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

# provides the browser for the test session
@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, request):
    is_headed = request.config.getoption("--headed")
    browser_name = request.config.getoption("--browser")

    if browser_name == "chromium":
        browser = playwright_instance.chromium.launch(headless=False, args=['--start-maximized'], slow_mo=600)
    elif browser_name == "firefox":
        browser = playwright_instance.firefox.launch(headless=False, args=['--start-maximized'], slow_mo=500)
    elif browser_name == "webkit":
        browser = playwright_instance.webkit.launch(headless=False, args=['--start-maximized'], slow_mo=500)
    else:
        raise ValueError(f"Browser '{browser_name}' not supported. update the `browser` fixture to handle it.")

    yield browser
    browser.close()


# provides a new page for each test
@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.set_default_timeout(15000)
    yield page
    context.close()

# load and provide test data
@pytest.fixture(scope="session")
def test_data():
    with open("test_data/test_data.json", "r") as f:
        data = json.load(f)["test_cases"]
    return data

# navigates to the singapore URL before each test
@pytest.fixture(scope="function")
def singapore_URL(page, test_data):
    page.goto(test_data["homepage_url"])
    return page

# New fixture to capture logs
@pytest.fixture(scope="function")
def logs(caplog):
    caplog.set_level(logging.INFO)
    yield caplog

# capture a screenshot and logs after every execution
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and "page" in item.funcargs:
        page = item.funcargs["page"]
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        test_name = item.name.replace("/", "_").replace("::", "__")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        outcome_label = "PASSED" if report.passed else "FAILED"
        screenshot_path = os.path.join(screenshots_dir, f"{test_name}_{outcome_label}_{timestamp}.png")

        try:
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"\nScreenshot saved: {screenshot_path}")

            if os.path.exists(screenshot_path):
                with open(screenshot_path, "rb") as image_file:
                    report.extra = getattr(report, "extra", [])
                    report.extra.append(extras.image(image_file.read()))

            # Check for logs and attach to report
            if "logs" in item.funcargs:
                caplog = item.funcargs["logs"]
                log_stream = io.StringIO()
                for record in caplog.records:
                    log_stream.write(f"{record.levelname}: {record.message}\n")
                if log_stream.getvalue():
                    report.extra.append(extras.text(log_stream.getvalue()))

        except Exception as e:
            print(f"\nCould not take screenshot: {e}")