import time

import pytest
from faker import Faker
from pages.home_page import HomePage
from pages.applicant_page import ApplicantPage
from pages.service_page import ServicePage
from pages.citizen_page import CitizenPage
from pages.birth_page import BirthPage
from pages.status_page import StatusPage

fake = Faker('ru_RU')


class TestBirthFlow:

    def test_birth_registration_full_flow(self, driver):
        HomePage(driver).open()
        HomePage(driver).click_login_as_user()

        applicant_page = ApplicantPage(driver)
        applicant_page.fill_applicant_page(
            surname=fake.last_name(),
            name=fake.first_name(),
            midname=fake.middle_name(),
            phone=fake.numerify('###########'),
            passport=fake.bothify('??######', letters='АВРСКЕОТН'),
            address=fake.address()
        )
        applicant_page.click_next()

        ServicePage(driver).select_birth()

        citizen_page = CitizenPage(driver)
        citizen_page.fill_citizen_page(
            surname=fake.last_name(),
            name=fake.first_name(),
            midname=fake.middle_name(),
            birthdate=fake.date_of_birth(minimum_age=18).strftime('%d%m%Y'),
            passport=fake.bothify('??######', letters='АВРСКЕОТН'),
            gender=fake.random_element(['муж', 'жен']),
            address=fake.address()
        )
        citizen_page.click_next()

        birth_page = BirthPage(driver)
        birth_page.fill_birth_page(
            place_of_birth=fake.address(),
            mother=' '.join([fake.first_name_female(), fake.last_name_female(), fake.middle_name_female()]),
            father=' '.join([fake.first_name_male(), fake.last_name_male(), fake.middle_name_male()]),
            granny=' '.join([fake.first_name_female(), fake.last_name_female(), fake.middle_name_female()]),
            grandad=' '.join([fake.first_name_male(), fake.last_name_male(), fake.middle_name_male()])
        )
        birth_page.click_finish()

        status_page = StatusPage(driver)

        assert status_page.is_status_displayed()
        assert status_page.is_success_message_displayed()