import time

import pytest
from faker import Faker
from pages.home_page import HomePage
from pages.applicant_page import ApplicantPage
from pages.service_page import ServicePage
from pages.citizen_page import CitizenPage
from pages.marriage_page import MarriagePage
from pages.status_page import StatusPage

fake = Faker('ru_RU')


class TestMarriageFlow:

    def test_marriage_registration_full_flow(self, driver):
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

        ServicePage(driver).select_marriage()

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

        marriage_page = MarriagePage(driver)
        marriage_page.fill_marriage_page(
            marriage_date=fake.date_of_birth(minimum_age=0, maximum_age=5).strftime('%d%m%Y'),
            new_surname=fake.last_name(),
            spouse_surname=fake.last_name(),
            spouse_name=fake.first_name(),
            spouse_midname=fake.middle_name(),
            spouse_birthdate=fake.date_of_birth(minimum_age=18).strftime('%d%m%Y'),
            spouse_passport=fake.bothify('??######', letters='АВРСКЕОТН')
        )
        marriage_page.click_finish()

        status_page = StatusPage(driver)

        assert status_page.is_status_displayed() is not None
        assert status_page.is_success_message_displayed() is not None