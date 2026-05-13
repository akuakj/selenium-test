import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class ServiceLocators:
    MARRIAGE_BUTTON = (By.XPATH, "//button[contains(text(), 'Регистрация брака')]")
    BIRTH_BUTTON = (By.XPATH, "//button[contains(text(), 'Регистрация рождения')]")

class ServicePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    @allure.step("Нажать Услуга регистрации брака")
    def select_marriage(self):
        self.wait.until(EC.element_to_be_clickable(ServiceLocators.MARRIAGE_BUTTON)).click()

    @allure.step("Нажать Услуга регистрации рождения")
    def select_birth(self):
        self.wait.until(EC.element_to_be_clickable(ServiceLocators.BIRTH_BUTTON)).click()