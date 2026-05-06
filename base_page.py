from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver, timeout=5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.default_timeout = timeout

    def find_element(self, locator, timeout=None):
        timeout = timeout if timeout is not None else self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            return f"элемент не найден {locator}"

    def click(self, locator, timeout=None):
        timeout_value = timeout if timeout is not None else self.default_timeout
        element = WebDriverWait(self.driver, timeout_value).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def input_text(self, locator, text, timeout=None):
        timeout_value = timeout if timeout is not None else self.default_timeout
        element = self.find_element(locator, timeout_value)
        element.clear()
        element.send_keys(text)