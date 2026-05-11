from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ApplicantForm(BasePage):

    SURNAME_USER = (By.XPATH, "//input[@placeholder='Введите фамилию (минимум 2 символа)']")
    NAME_USER = (By.XPATH, "//input[@placeholder='Введите имя (минимум 2 символа)']")
    MIDNAME_USER = (By.XPATH, "//input[@placeholder='Введите отчество (минимум 5 символов)']")
    PHONE_USER = (By.XPATH, "//input[@placeholder='Введите номер телефона (не более 11 символов)']")
    PASSPORT_USER = (By.XPATH, "//input[@placeholder='Введите номер паспорта (не более 8 символов)']")
    ADDRESS_USER = (By.XPATH, "//input[@placeholder='Введите адрес прописки']")

    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Далее')]")

    def __init__(self, driver):
        super().__init__(driver)

    def fill_surname(self, surname):
        self.input_text(self.SURNAME_USER, surname)

    def fill_name(self, name):
        self.input_text(self.NAME_USER, name)

    def fill_midname(self, midname):
        self.input_text(self.MIDNAME_USER, midname)

    def fill_phone(self, phone):
        self.input_text(self.PHONE_USER, phone)

    def fill_passport(self, passport):
        self.input_text(self.PASSPORT_USER, passport)

    def fill_address(self, address):
        self.input_text(self.ADDRESS_USER, address)

    def click_next(self):
        self.click(self.NEXT_BUTTON)
        print("шаг 1 -> переход на след форму")