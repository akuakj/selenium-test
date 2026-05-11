from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class StatusLocators:
    TEXT_THX_FOR_CONTACT = (By.XPATH, "//span[contains(text(), 'Спасибо за обращение!')]")
    TEXT_STATUS = (By.XPATH, "//span[contains(text(), 'отправлена на рассмотрение')]")

class StatusPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def is_success_message_displayed(self):
        element = self.wait.until(EC.presence_of_element_located(StatusLocators.TEXT_THX_FOR_CONTACT))
        return element is not None

    def is_status_displayed(self):
        element = self.wait.until(EC.presence_of_element_located(StatusLocators.TEXT_STATUS))
        return element is not None
