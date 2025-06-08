import pytest
import tempfile
from datetime import datetime

import functools
import time
import sys
import os.path
from pathlib import Path
import inspect
import pandas

# Provide multiple browser support for running tests
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from test_util.config import TEST_ENV

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))
EXCEL_DATA = Path(__file__).parents[1]/'test_data/testdata.xlsx'


def get_excel_test_data(sheet_name):
    """Read excel and get the needed test data"""
    excel_data_df = pandas.read_excel(EXCEL_DATA, sheet_name=sheet_name)
    json_list = excel_data_df.to_dict('records')
    return json_list


def pytest_generate_tests(metafunc):
    """Check if a fixture is requested, then get the data"""
    if "form_test" in metafunc.fixturenames:
        metafunc.parametrize("form_test", get_excel_test_data('form_test'))


#
def pytest_addoption(parser):
    """
    Add option to accept different kind of browser to run the test. Default is set to chrome. Supports firefox
    """
    parser.addoption(
        "--driver", action="store", default="chrome", help="default: chrome, option: firefox"
    )


@pytest.fixture(scope='session')
def create_temp_dir():
    """
    Temporary directory for testing downloads. Easier to located files to be tested and clean up after the test
    """
    temp_dir = tempfile.TemporaryDirectory()
    yield temp_dir.name
    temp_dir.cleanup()


@pytest.fixture(scope='session')
def web_driver(request, create_temp_dir):
    selected_driver = request.config.getoption("--driver")
    driver = None
    if selected_driver == 'chrome':
        chrome_options = ChromeOptions()
        if not TEST_ENV.webdriver_visible:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--enable-precise-memory-info")
        chrome_options.add_argument('lang=en')
        chrome_options.add_argument("--disable-features=InsecureDownloadWarnings")
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        default_download_location = {'download.default_directory': create_temp_dir}
        chrome_options.add_experimental_option('prefs', default_download_location)
        driver = Chrome(options=chrome_options)
        driver.maximize_window()
    elif selected_driver == 'firefox':
        firefox_options = FirefoxOptions()
        if not TEST_ENV.webdriver_visible:
            firefox_options.headless = True
        firefox_options.set_preference("browser.download.folderList", 2)
        firefox_options.set_preference("browser.download.dir", create_temp_dir)
        firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_options.set_preference("browser.download.viewableInternally.enabledTypes", "")
        firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                       "application/octet-stream,application/vnd.ms-excel,application/xml,text/xml")
        firefox_options.add_argument("--window-size=1920,1080")
        firefox_options.add_argument('--ignore-certificate-errors')
        driver = Firefox(options=firefox_options)
        driver.maximize_window()

    # Return the driver object at the end of setup
    yield driver

    # For cleanup, quit the driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Store the results of each test phase to check if the test fails for reporting
    """
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    """
    Check if the test fails and take a screenshot of the state of the UI
    """
    yield
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.name)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.node.funcargs['web_driver']
            take_screenshot(driver, request.node.name)


def take_screenshot(web_driver, test_name):
    screenshot_path = f'{path}/../results/screenshots/Functional_Test_{datetime.today().strftime("%Y-%m-%d")}/'
    file_name = f'{datetime.today().strftime("%H%M%S")}_{test_name}'

    if not os.path.exists(screenshot_path):
        os.makedirs(screenshot_path)

    web_driver.save_screenshot(f'{screenshot_path}/{file_name}.png')


def print_timing(web_driver, interaction=None, ):
    assert interaction is not None, "Interaction name is not passed to print_timing decorator"

    def deco_wrapper(func):
        # noinspection PyBroadException
        @functools.wraps(func)
        def wrapper():
            start = time.time()
            error_msg = 'Success'
            memory_usage = 0
            backend_performance = 0
            frontend_performance = 0
            latency = 0
            server_response_time = 0
            page_load_time = 0
            transfer_page_download_time = 0
            try:
                func()
                json_obj = web_driver.execute_script("return window.performance.memory.usedJSHeapSize")
                memory_usage = round(json_obj / (1024 * 1024), 2)
                success = True

                navigation_start = web_driver.execute_script("return window.performance.timing.navigationStart")
                response_start = web_driver.execute_script("return window.performance.timing.responseStart")
                dom_complete = web_driver.execute_script("return window.performance.timing.domComplete")
                fetch_start = web_driver.execute_script("return window.performance.timing.fetchStart")
                request_start = web_driver.execute_script("return window.performance.timing.requestStart")
                load_event_start = web_driver.execute_script("return window.performance.timing.loadEventStart")
                response_end = web_driver.execute_script("return window.performance.timing.responseEnd")
                backend_performance = response_start - navigation_start
                frontend_performance = dom_complete - response_start
                latency = response_start - fetch_start
                server_response_time = response_start - request_start
                page_load_time = load_event_start - navigation_start
                transfer_page_download_time = response_end - response_start

            except Exception:
                success = False
                # https://docs.python.org/2/library/sys.html#sys.exc_info
                exc_type, full_exception = sys.exc_info()[:2]
                error_msg = f"Failed measure: {interaction} - {exc_type.__name__}"
            end = time.time()
            timing = str(int((end - start) * 1000))
            timestamp = round(time.time() * 1000)

            print(f"{timestamp},{timing},{memory_usage},{interaction},{error_msg},{success},{backend_performance},"
                  f"{frontend_performance},{latency}, {server_response_time},{page_load_time},"
                  f"{transfer_page_download_time}")
            assert success, error_msg
        return wrapper
    return deco_wrapper

