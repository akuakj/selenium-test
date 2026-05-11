import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class CitizenLocators:
    CITIZEN_SURNAME = (By.XPATH, "(//input[@maxlength='100'])[1]")
    CITIZEN_NAME = (By.XPATH, "(//input[@maxlength='100'])[2]")
    CITIZEN_MIDNAME = (By.XPATH, "(//input[@maxlength='100'])[3]")
    CITIZEN_DATE_OF_BIRTH = (By.XPATH, "//input[@type='date']")
    CITIZEN_PASSPORT = (By.XPATH, "//input[@maxlength='8']")
    CITIZEN_GENDER = (By.XPATH, "//input[@maxlength='4']")
    CITIZEN_ADDRESS = (By.XPATH, "//input[@placeholder='Введите адрес прописки']")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Далее')]")

class CitizenPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def fill_surname(self, surname):
        field = self.wait.until(EC.presence_of_element_located(CitizenLocators.CITIZEN_SURNAME))
        field.clear()
        field.send_keys(surname)
        return self

    def fill_name(self, name):
        field = self.wait.until(EC.presence_of_element_located(CitizenLocators.CITIZEN_NAME))
        field.clear()
        field.send_keys(name)
        return self

    def fill_midname(self, midname):
        field = self.wait.until(EC.presence_of_element_located(CitizenLocators.CITIZEN_MIDNAME))
        field.clear()
        field.send_keys(midname)
        return self

    def fill_birthdate(self, birthdate):
        field = self.wait.until(EC.presence_of_element_located(CitizenLocators.CITIZEN_DATE_OF_BIRTH))
        field.clear()
        field.send_keys(birthdate)
        return self

    def fill_passport(self, passport):
        field = self.wait.until(EC.presence_of_element_located(CitizenLocators.CITIZEN_PASSPORT))
        field.clear()
        field.send_keys(passport)
        return self

    def fill_gender(self, gender):
        field = self.wait.until(EC.presence_of_element_located(CitizenLocators.CITIZEN_GENDER))
        field.clear()
        field.send_keys(gender)
        return self

    def fill_address(self, address):
        field = self.wait.until(EC.presence_of_element_located(CitizenLocators.CITIZEN_ADDRESS))
        field.clear()
        field.send_keys(address)
        return self

    def fill_citizen_page(self, surname, name, midname, birthdate, passport, gender, address):
        self.fill_surname(surname)
        self.fill_name(name)
        self.fill_midname(midname)
        self.fill_birthdate(birthdate)
        self.fill_passport(passport)
        self.fill_gender(gender)
        self.fill_address(address)
        return self

    def click_next(self):
        button = self.wait.until(EC.element_to_be_clickable(CitizenLocators.NEXT_BUTTON))
        button.click()

    def is_next_button_disabled(self):
        button = self.wait.until(EC.presence_of_element_located(CitizenLocators.NEXT_BUTTON))
        disabled = button.get_attribute("disabled")
        return disabled is not None and disabled != 'false'

    def is_next_button_enabled(self):
        return not self.is_next_button_disabled()