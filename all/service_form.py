from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ServiceForm(BasePage):

    MARRIAGE_BUTTON = (By.XPATH, "//button[contains(text(), 'Регистрация брака')]")
    BIRTH_BUTTON = (By.XPATH, "//button[contains(text(), 'Регистрация рождения')]")

    def __init__(self, driver):
        super().__init__(driver)

    def select_marriage(self):
        self.click(self.MARRIAGE_BUTTON)
        print("шаг 2: выбрана услуга регистрации брака")

    def select_birth(self):
        self.click(self.BIRTH_BUTTON)
        print("шаг 2: выбрана услуга регистрации рождения")