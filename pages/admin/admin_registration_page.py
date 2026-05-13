from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AdminRegistrationLocators:
    ADMIN_SURNAME = (By.XPATH, "(//input[@maxlength='100'])[1]")
    ADMIN_NAME = (By.XPATH, '(//input[@maxlength="100"])[2]')
    ADMIN_MIDNAME = (By.XPATH, '(//input[@maxlength="100"])[3]')
    ADMIN_PHONE = (By.XPATH, '//input[@maxlength="11"]')
    ADMIN_PASSPORT = (By.XPATH, '//input[@maxlength="8"]')
    ADMIN_DATE_OF_BIRTH = (By.XPATH, "//input[@type='date']")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Далее')]")


class AdminRegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def fill_surname(self, surname):
        field = self.wait.until(EC.presence_of_element_located(AdminRegistrationLocators.ADMIN_SURNAME))
        field.clear()
        field.send_keys(surname)
        return self

    def fill_name(self, name):
        field = self.wait.until(EC.presence_of_element_located(AdminRegistrationLocators.ADMIN_NAME))
        field.clear()
        field.send_keys(name)
        return self

    def fill_midname(self, midname):
        field = self.wait.until(EC.presence_of_element_located(AdminRegistrationLocators.ADMIN_MIDNAME))
        field.clear()
        field.send_keys(midname)
        return self

    def fill_phone(self, phone):
        field = self.wait.until(EC.presence_of_element_located(AdminRegistrationLocators.ADMIN_PHONE))
        field.clear()
        field.send_keys(phone)
        return self

    def fill_passport(self, passport):
        field = self.wait.until(EC.presence_of_element_located(AdminRegistrationLocators.ADMIN_PASSPORT))
        field.clear()
        field.send_keys(passport)
        return self

    def fill_birthday(self, birthdate):
        field = self.wait.until(EC.presence_of_element_located(AdminRegistrationLocators.ADMIN_DATE_OF_BIRTH))
        field.clear()
        field.send_keys(birthdate)
        return self

    def fill_admin_page(self, surname, name, midname, phone, passport, birthdate):
        self.fill_surname(surname)
        self.fill_name(name)
        self.fill_midname(midname)
        self.fill_phone(phone)
        self.fill_passport(passport)
        self.fill_birthday(birthdate)
        return self

    def click_next(self):
        button = self.wait.until(EC.element_to_be_clickable(AdminRegistrationLocators.NEXT_BUTTON))
        button.click()

    def check_next_button_disabled(self):
        button = self.wait.until(EC.presence_of_element_located(AdminRegistrationLocators.NEXT_BUTTON))
        disabled = button.get_attribute("disabled")
        return disabled is not None and disabled != 'false', "Кнопка Далее должна быть неактивна"

    def check_next_button_enabled(self):
        button = self.wait.until(EC.presence_of_element_located(AdminRegistrationLocators.NEXT_BUTTON))
        disabled = button.get_attribute("disabled")
        return disabled is None or disabled == 'false', "Кнопка Далее должна быть активна"




