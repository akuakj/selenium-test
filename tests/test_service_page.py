import pytest
from faker import Faker
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.applicant_page import ApplicantPage
from pages.service_page import ServicePage
from pages.citizen_page import CitizenLocators


fake = Faker('ru_RU')

def go_to_service_page(driver):
    HomePage(driver).open()
    HomePage(driver).click_login_as_user()

    applicant_page = ApplicantPage(driver)
    applicant_page.fill_applicant_page(
        surname=fake.last_name(),
        name = fake.first_name(),
        midname = fake.middle_name(),
        phone = fake.numerify('########'),
        passport = fake.bothify('??######', letters='АВРСКЕОТН'),
        address = fake.address()
    )
    applicant_page.click_next()
    return ServicePage(driver)

class TestServicePage:
    def test_marriage_service_opens_citizen_page(self, driver):
        go_to_service_page(driver).select_marriage()

        field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(CitizenLocators.CITIZEN_SURNAME)
        )
        assert field is not None

    def test_birth_service_opens_citizen_page(self, driver):
        go_to_service_page(driver).select_birth()

        field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(CitizenLocators.CITIZEN_SURNAME)
        )
        assert field is not None

