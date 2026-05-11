from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MarriageLocators:
    MARRIAGE_DATE = (By.XPATH, "(//input[@type='date'])[1]")
    NEW_SURNAME = (By.XPATH, "(//input[@maxlength='50'])[1]")
    SPOUSE_SURNAME = (By.XPATH, "(//input[@maxlength='50'])[2]")
    SPOUSE_NAME = (By.XPATH, "(//input[@maxlength='20'])[1]")
    SPOUSE_MIDNAME = (By.XPATH, "(//input[@maxlength='20'])[2]")
    SPOUSE_BIRTHDATE = (By.XPATH, "(//input[@type='date'])[2]")
    SPOUSE_PASSPORT = (By.XPATH, "//input[@maxlength='8']")
    FINISH_BUTTON = (By.XPATH, "//button[contains(text(), 'Завершить')]")

class MarriagePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def fill_marriage_date(self, date_of_marriage):
        field = self.wait.until(EC.presence_of_element_located(MarriageLocators.MARRIAGE_DATE))
        field.clear()
        field.send_keys(date_of_marriage)
        return self

    def fill_new_surname(self, new_surname):
        field = self.wait.until(EC.presence_of_element_located(MarriageLocators.NEW_SURNAME))
        field.clear()
        field.send_keys(new_surname)
        return self

    def fill_spouse_surname(self, spouse_surname):
        field = self.wait.until(EC.presence_of_element_located(MarriageLocators.SPOUSE_SURNAME))
        field.clear()
        field.send_keys(spouse_surname)
        return self

    def fill_spouse_name(self, spouse_name):
        field = self.wait.until(EC.presence_of_element_located(MarriageLocators.SPOUSE_NAME))
        field.clear()
        field.send_keys(spouse_name)
        return self

    def fill_spouse_midname(self, spouse_midname):
        field = self.wait.until(EC.presence_of_element_located(MarriageLocators.SPOUSE_MIDNAME))
        field.clear()
        field.send_keys(spouse_midname)
        return self

    def fill_spouse_birthdate(self, spouse_birthdate):
        field = self.wait.until(EC.presence_of_element_located(MarriageLocators.SPOUSE_BIRTHDATE))
        field.clear()
        field.send_keys(spouse_birthdate)
        return self

    def fill_spouse_passport(self, spouse_passport):
        field = self.wait.until(EC.presence_of_element_located(MarriageLocators.SPOUSE_PASSPORT))
        field.clear()
        field.send_keys(spouse_passport)
        return self

    def fill_marriage_page(self, marriage_date, new_surname, spouse_surname, spouse_name, spouse_midname, spouse_birthdate, spouse_passport):
        self.fill_marriage_date(marriage_date)
        self.fill_new_surname(new_surname)
        self.fill_spouse_surname(spouse_surname)
        self.fill_spouse_name(spouse_name)
        self.fill_spouse_midname(spouse_midname)
        self.fill_spouse_birthdate(spouse_birthdate)
        self.fill_spouse_passport(spouse_passport)

    def click_finish(self):
        button = self.wait.until(EC.element_to_be_clickable(MarriageLocators.FINISH_BUTTON))
        button.click()


    def is_finish_button_disabled(self):
        button = self.wait.until(EC.presence_of_element_located(MarriageLocators.FINISH_BUTTON))
        disabled = button.get_attribute("disabled")
        return disabled is not None and disabled != 'false'

    def is_finish_button_enabled(self):
        return not self.is_finish_button_disabled()