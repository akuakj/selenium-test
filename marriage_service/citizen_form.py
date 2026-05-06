from selenium.webdriver.common.by import By
from base_page import BasePage

class CitizenForm(BasePage):

    SURNAME_CITIZEN = (By.XPATH, "(//input[@maxlength='100'])[1]")
    NAME_CITIZEN = (By.XPATH, "(//input[@maxlength='100'])[2]")
    MIDNAME_CITIZEN = (By.XPATH, "(//input[@maxlength='100'])[3]")
    DATE_CITIZEN = (By.XPATH, "//input[@type='date']")
    PASSPORT_CITIZEN = (By.XPATH, "//input[@maxlength='8']")
    GENDER_CITIZEN = (By.XPATH, "//input[@maxlength='4']")
    ADDRESS_CITIZEN = (By.XPATH, "//input[@placeholder='Введите адрес прописки']")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Далее')]")

    def __init__(self, driver):
        super().__init__(driver)

    def fill_surname(self, surname):
        self.input_text(self.SURNAME_CITIZEN, surname)

    def fill_name(self, name):
        self.input_text(self.NAME_CITIZEN, name)

    def fill_midname(self, midname):
        self.input_text(self.MIDNAME_CITIZEN, midname)

    def fill_birthdate(self, birthdate):
        self.input_text(self.DATE_CITIZEN, birthdate)

    def fill_passport(self, passport):
        self.input_text(self.PASSPORT_CITIZEN, passport)

    def fill_gender(self, gender):
        self.input_text(self.GENDER_CITIZEN, gender)

    def fill_address(self, address):
        self.input_text(self.ADDRESS_CITIZEN, address)

    def click_next(self):
        self.click(self.NEXT_BUTTON)
        print("шаг 3 -> переход на след форму")

