from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


DRIVER = None


def initialize_chrome_driver():
    global DRIVER
    options = Options()
    options.headless = True
    DRIVER = webdriver.Chrome(options=options, executable_path="./selenium_driver/chromedriver")


def go_to_url(url):
    DRIVER.get(url)


def get_web_element(rel_xpath, root=None):
    try:
        if root == None:
            return DRIVER.find_element_by_xpath(rel_xpath)
        return root.find_element_by_xpath(rel_xpath)
    except NoSuchElementException:
        return None


def get_web_elements(rel_xpath, root=None):
    try:
        if root == None:
            return DRIVER.find_elements_by_xpath(rel_xpath)
        return root.find_elements_by_xpath(rel_xpath)
    except NoSuchElementException:
        return None


def disconnect():
    DRIVER.quit()