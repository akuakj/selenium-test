from selenium.webdriver.common.by import By
from base_page import BasePage

class MarriageForm(BasePage):

    MARRIAGE_DATE = (By.XPATH, "(//input[@type='date'])[1]")
    NEW_SURNAME = (By.XPATH, "(//input[@maxlength='50'])[1]")
    SPOUSE_SURNAME = (By.XPATH, "(//input[@maxlength='50'])[2]")
    SPOUSE_NAME = (By.XPATH, "(//input[@maxlength='20'])[1]")
    SPOUSE_MIDNAME = (By.XPATH, "(//input[@maxlength='20'])[2]")
    SPOUSE_BIRTHDATE = (By.XPATH, "(//input[@type='date'])[2]")
    SPOUSE_PASSPORT = (By.XPATH, "//input[@maxlength='8']")
    FINISH_BUTTON        = (By.XPATH, "//button[contains(text(), 'Завершить')]")

    def __init__(self, driver):
        super().__init__(driver)

    def fill_date(self, date):
        self.input_text(self.MARRIAGE_DATE, date)

    def fill_new_surname(self, new_surname):
        self.input_text(self.NEW_SURNAME, new_surname)

    def fill_spouse_surname(self, surname):
        self.input_text(self.SPOUSE_SURNAME, surname)

    def fill_spouse_name(self, name):
        self.input_text(self.SPOUSE_NAME    , name)

    def fill_spouse_midname(self, midname):
        self.input_text(self.SPOUSE_MIDNAME, midname)

    def fill_spouse_birthdate(self, birthdate):
        self.input_text(self.SPOUSE_BIRTHDATE, birthdate)

    def fill_spouse_passport(self, passport):
        self.input_text(self.SPOUSE_PASSPORT, passport)

    def click_finish(self):
        self.click(self.FINISH_BUTTON)
        print("Шаг 4 → нажата кнопка 'Завершить'")