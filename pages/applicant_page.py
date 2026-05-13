from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ApplicantLocators:
    SURNAME_USER = (By.XPATH, "//input[@placeholder='Введите фамилию (минимум 2 символа)']")
    NAME_USER = (By.XPATH, "//input[@placeholder='Введите имя (минимум 2 символа)']")
    MIDNAME_USER = (By.XPATH, "//input[@placeholder='Введите отчество (минимум 5 символов)']")
    PHONE_USER = (By.XPATH, "//input[@placeholder='Введите номер телефона (не более 11 символов)']")
    PASSPORT_USER = (By.XPATH, "//input[@placeholder='Введите номер паспорта (не более 8 символов)']")
    ADDRESS_USER = (By.XPATH, "//input[@placeholder='Введите адрес прописки']")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Далее')]")


class ApplicantPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def fill_surname(self, surname):
        field = self.wait.until(EC.presence_of_element_located(ApplicantLocators.SURNAME_USER))
        field.clear()
        field.send_keys(surname)
        return self

    def fill_name(self, name):
        field = self.wait.until(EC.presence_of_element_located(ApplicantLocators.NAME_USER))
        field.clear()
        field.send_keys(name)
        return self

    def fill_midname(self, midname):
        field = self.wait.until(EC.presence_of_element_located(ApplicantLocators.MIDNAME_USER))
        field.clear()
        field.send_keys(midname)
        return self

    def fill_phone(self, phone):
        field = self.wait.until(EC.presence_of_element_located(ApplicantLocators.PHONE_USER))
        field.clear()
        field.send_keys(phone)
        return self

    def fill_passport(self, passport):
        field = self.wait.until(EC.presence_of_element_located(ApplicantLocators.PASSPORT_USER))
        field.clear()
        field.send_keys(passport)
        return self

    def fill_address(self, address):
        field = self.wait.until(EC.presence_of_element_located(ApplicantLocators.ADDRESS_USER))
        field.clear()
        field.send_keys(address)
        return self

    def fill_applicant_page(self, surname, name, midname, phone, passport, address):
        self.fill_surname(surname)
        self.fill_name(name)
        self.fill_midname(midname)
        self.fill_phone(phone)
        self.fill_passport(passport)
        self.fill_address(address)
        return self


    def click_next(self):
        button = self.wait.until(EC.element_to_be_clickable(ApplicantLocators.NEXT_BUTTON))
        button.click()

    def check_next_button_disabled(self):
        button = self.wait.until(EC.presence_of_element_located(ApplicantLocators.NEXT_BUTTON))
        disabled = button.get_attribute("disabled")
        assert disabled is not None and disabled != 'false',  "Кнопка Далее должна быть неактивна"

    def check_next_button_enabled(self):
        button = self.wait.until(EC.presence_of_element_located(ApplicantLocators.NEXT_BUTTON))
        disabled = button.get_attribute("disabled")
        assert disabled is None or disabled == 'false', "Кнопка Далее должна быть активна"


