from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class HomeLocators:
    LOGIN_AS_USER_BUTTON = (By.XPATH, '//button[contains(text(), "Войти как пользователь")]')
    LOGIN_AS_ADMIN_BUTTON = (By.XPATH, '//button[contains(text(), "Войти как администратор")]')

class HomePage:
    BASE_URL = "https://user:senlatest@regoffice.senla.eu"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,5)

    def open(self):
        self.driver.get(self.BASE_URL)

    @allure.step("Нажать Войти как пользователь")
    def click_login_as_user(self):
        self.wait.until(EC.element_to_be_clickable(HomeLocators.LOGIN_AS_USER_BUTTON)).click()

    @allure.step("Нажать Войти как администратор")
    def click_login_as_admin(self):
        self.wait.until(EC.element_to_be_clickable(HomeLocators.LOGIN_AS_ADMIN_BUTTON)).click()
