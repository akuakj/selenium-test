import time
from selenium import webdriver
from home_page import HomePage
from applicant_form import ApplicantForm
from service_form import ServiceForm

from marriage_service.citizen_form import CitizenForm as MarriageCitizenForm
from marriage_service.marriage_form import MarriageForm

from birth_service.citizen_form import CitizenForm as BirthCitizenForm
from birth_service.birth_form import BirthForm


class TestRegistration:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def teardown_method(self):
        time.sleep(3)
        self.driver.quit()

    def test_marriage_registration(self):
        self.driver.get("https://user:senlatest@regoffice.senla.eu")

        # главная страница
        HomePage(self.driver).click_login_as_user()
        time.sleep(2)

        # данные заявителя
        applicant = ApplicantForm(self.driver)
        applicant.fill_surname("Ivanov")
        applicant.fill_name("Ivan")
        applicant.fill_midname("Ivanovich")
        applicant.fill_phone("1234567890")
        applicant.fill_passport("AB123456")
        applicant.fill_address("Брест, улица Машерова 12")

        time.sleep(1)
        applicant.click_next()


        # выбор услуги
        ServiceForm(self.driver).select_marriage()

        # данные гражданина
        citizen = MarriageCitizenForm(self.driver)
        citizen.fill_surname("Ivanov")
        citizen.fill_name("Ivan")
        citizen.fill_midname("Ivanovich")
        citizen.fill_birthdate("11.04.1999")
        citizen.fill_passport("AB123456")
        citizen.fill_gender("M")
        citizen.fill_address("Брест, улица Машерова 12")

        time.sleep(1)
        citizen.click_next()

        # данные брака
        marriage = MarriageForm(self.driver)
        marriage.fill_date("01072026")
        marriage.fill_new_surname("Ivanova")
        marriage.fill_spouse_surname("Ivanova")
        marriage.fill_spouse_name("Nastya")
        marriage.fill_spouse_midname("Petrovna")
        marriage.fill_spouse_birthdate("20031993")
        marriage.fill_spouse_passport("AB87654")

        time.sleep(1)
        marriage.click_finish()

        # проверка результата
        time.sleep(2)



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

        time.sleep(1)
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

        time.sleep(1)
        citizen.click_next()

        birth = BirthForm(self.driver)
        birth.fill_place_of_birth("г. Минск")
        birth.fill_mother("mother")
        birth.fill_father("father")
        birth.fill_granny("granny")
        birth.fill_granddad("granddad")

        time.sleep(1)
        birth.click_finish()


        time.sleep(2)






if __name__ == "__main__":
    test = TestRegistration()

    test.setup_method()
    test.test_marriage_registration()

    test.test_birth_registration()
    test.teardown_method()