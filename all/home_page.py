from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    LOGIN_AS_USER_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти как пользователь')]")

    def __init__(self, driver):
        super().__init__(driver)

    def click_login_as_user(self):
        self.click(self.LOGIN_AS_USER_BUTTON)
        print("Выбрано: войти как пользователь")


