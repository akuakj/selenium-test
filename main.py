import time
from selenium import webdriver
from home_page import HomePage
from applicant_form import ApplicantForm
from service_form import ServiceForm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from marriage_service.citizen_form import CitizenForm as MarriageCitizenForm
from marriage_service.marriage_form import MarriageForm

from birth_service.citizen_form import CitizenForm as BirthCitizenForm
from birth_service.birth_form import BirthForm


class TestRegistration:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        time.sleep(3)
        self.driver.quit()

    def test_marriage_registration(self):
        self.driver.get("https://user:senlatest@regoffice.senla.eu")

        # главная страница
        HomePage(self.driver).click_login_as_user()

        # данные заявителя
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Введите фамилию (минимум 2 символа)']")
        ))
        applicant = ApplicantForm(self.driver)
        applicant.fill_surname("Ivanov")
        applicant.fill_name("Ivan")
        applicant.fill_midname("Ivanovich")
        applicant.fill_phone("1234567890")
        applicant.fill_passport("AB123456")
        applicant.fill_address("Брест, улица Машерова 12")

        applicant.click_next()


        # выбор услуги
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Регистрация брака')]")
        ))
        ServiceForm(self.driver).select_marriage()


        # данные гражданина
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//input[@maxlength='100'])[1]")
        ))
        citizen = MarriageCitizenForm(self.driver)
        citizen.fill_surname("Ivanov")
        citizen.fill_name("Ivan")
        citizen.fill_midname("Ivanovich")
        citizen.fill_birthdate("11.04.1999")
        citizen.fill_passport("AB123456")
        citizen.fill_gender("M")
        citizen.fill_address("Брест, улица Машерова 12")

        citizen.click_next()

        # данные брака
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='дд/мм/гггг']")
        ))
        marriage = MarriageForm(self.driver)
        marriage.fill_date("01072026")
        marriage.fill_new_surname("Ivanova")
        marriage.fill_spouse_surname("Ivanova")
        marriage.fill_spouse_name("Nastya")
        marriage.fill_spouse_midname("Petrovna")
        marriage.fill_spouse_birthdate("20031993")
        marriage.fill_spouse_passport("AB87654")

        marriage.click_finish()


    def test_birth_registration(self):
        self.driver.get("https://user:senlatest@regoffice.senla.eu")

        HomePage(self.driver).click_login_as_user()

        applicant = ApplicantForm(self.driver)
        applicant.fill_name("Petr")
        applicant.fill_surname("Petrov")
        applicant.fill_midname("Petrovich")
        applicant.fill_phone("801235612")
        applicant.fill_passport("AB43243")
        applicant.fill_address("Минск, улица Машерова 12")

        applicant.click_next()

        ServiceForm(self.driver).select_birth()

        citizen = BirthCitizenForm(self.driver)
        citizen.fill_surname("Ivanov")
        citizen.fill_name("Ivan")
        citizen.fill_midname("Ivanovich")
        citizen.fill_birthdate("06.05.2026")
        citizen.fill_passport("AB123456")
        citizen.fill_gender("M")
        citizen.fill_address("Минск, улица Машерова 12")

        citizen.click_next()

        birth = BirthForm(self.driver)
        birth.fill_place_of_birth("г. Минск")
        birth.fill_mother("mother")
        birth.fill_father("father")
        birth.fill_granny("granny")
        birth.fill_granddad("granddad")

        birth.click_finish()



if __name__ == "__main__":
    test = TestRegistration()

    test.setup_method()
    test.test_marriage_registration()

    test.test_birth_registration()
    test.teardown_method()