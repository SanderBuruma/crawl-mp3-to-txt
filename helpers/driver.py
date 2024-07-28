from selenium import webdriver

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime, timedelta
import os


def get_chrome_driver(headless=False):
    """
    Gets the chrome driver for the use of automatic browsing and crawling
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    srvc = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=srvc, options=options)
    driver.set_window_size(1920, 1080)

    return driver

def wait_for_element(driver, by: By, selector: str, timeout = 30):
    """
    Waits for the element given by `selector` to appear in the browser and returns it
    :param driver: The webdriver being used
    :param by: The type of selector being passed, ie. ID, CSS_CLASS, XPATH, etc
    :param timeout: timeout period in seconds, It's set to 10 by default
    """
    try:
        element: WebElement = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
    except TimeoutException as e:
        print("Timeout waiting for element matching selector '{0}' - By '{1}' to appear".format(selector, by))
        e.add_note("Timeout waiting for element matching selector '{0}' - By '{1}' to appear".format(selector, by))
        raise e
    return element

def wait_for_partial_name(driver, selector: str, timeout = 30):
    """
    Waits for the element given by a partial Name `selector` to appear in the browser and returns it
    :param driver: The webdriver being used
    :param by: The type of selector being passed, ie. ID, CSS_CLASS, XPATH, etc
    :param timeout: timeout period in seconds, It's set to 10 by default
    """
    element: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@name, '"+selector+"')]"))
    )
    return element

def wait_for_and_click(driver, by: By, selector: str, timeout = 30):
    """
    Same as wait_for_element but clicks the element as well
    """
    clickable_button = wait_for_element(driver, by, selector, timeout)
    clickable_button.click()
    return clickable_button

def generate_screenshot_path(testName, date: datetime):
    timestamp = (date or datetime.now()).strftime("%Y%m%d%H%M")
    screenshot_file = f"screenshots/{timestamp}{testName}.png"
    return screenshot_file

def take_screenshot(driver, testName, date: datetime):
    screenshot_file = generate_screenshot_path(testName, date)
    driver.save_screenshot(screenshot_file)

    # Define the directory where screenshots are stored
    screenshot_dir = "screenshots"

    # Check that screenshots dir exists, if not create it
    if not os.path.exists(screenshot_dir):
        os.mkdir(screenshot_dir)

    # Get the current date
    current_date = datetime.now()

