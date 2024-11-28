"""
Environment for Behave Testing
"""
from os import getenv
from selenium import webdriver
import logging

# Constants for environment variables
WAIT_SECONDS = int(getenv('WAIT_SECONDS', '30'))
BASE_URL = getenv('BASE_URL', 'http://localhost:8080')
DRIVER = getenv('DRIVER', 'firefox').lower()

def before_all(context):
    """ Executed once before all tests """
    context.base_url = BASE_URL
    context.wait_seconds = WAIT_SECONDS
    if 'firefox' in DRIVER:
        context.driver = get_firefox()
    else:
        context.driver = get_chrome()
    context.browser = context.driver  # Add this line to set context.browser
    context.driver.implicitly_wait(context.wait_seconds)
    context.config.setup_logging()

def after_all(context):
    """ Executed once after all tests """
    logging.info("Closing the browser...")
    context.driver.quit()
    logging.info("Browser closed.")

######################################################################
# Utility functions to create web drivers
######################################################################

def get_chrome():
    """Creates a headless Chrome driver"""
    logging.info("Setting up Chrome driver...")
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable to older versions of Chrome
    options.add_argument("--window-size=1920,1080")  # Optional: Set screen size for headless mode

    # Provide chromedriver executable path if not in PATH
    return webdriver.Chrome(options=options)

def get_firefox():
    """Creates a headless Firefox driver"""
    logging.info("Setting up Firefox driver...")
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--window-size=1920,1080")  # Optional: Set screen size for headless mode

    # Provide geckodriver executable path if not in PATH
    return webdriver.Firefox(options=options)
