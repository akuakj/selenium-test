import pytest
from pages.home_page import HomePage
from pages.applicant_page import ApplicantPage
from pages.citizen_page import CitizenPage
from pages.service_page import ServicePage
from faker import Faker
import time

fake = Faker('ru_RU')

def go_to_citizen_page(driver):
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
    ServicePage(driver).select_marriage()
    return CitizenPage(driver)

def valid_values():
    return dict (
        surname = fake.last_name(),
        name = fake.first_name(),
        midname = fake.middle_name(),
        birthdate = fake.date_of_birth(minimum_age=16).strftime('%d.%m.%Y'),
        passport = fake.bothify('??######', letters='АВРОНТСК'),
        gender = fake.random_element(['муж', 'жен', 'м', 'ж']),
        address = fake.address()
    )

class TestCitizenPage:
    def test_fill_citizen_page_with_all_valid_values(self, driver):
        citizen_page = go_to_citizen_page(driver)
        values = valid_values()
        citizen_page.fill_citizen_page(**values)
        assert citizen_page.is_next_button_enabled()

    def test_fill_citizen_page_without_surname(self, driver):
        citizen_page = go_to_citizen_page(driver)
        values = valid_values()
        values['surname'] = ''
        citizen_page.fill_citizen_page(**values)
        assert citizen_page.is_next_button_disabled()

    @pytest.mark.negative
    def test_fill_citizen_page_with_future_birthdate(self, driver):
        citizen_page = go_to_citizen_page(driver)
        values = valid_values()
        values['birthdate'] = '10.03.3036'
        citizen_page.fill_citizen_page(**values)
        assert citizen_page.is_next_button_disabled()

    def test_fill_citizen_page_without_gender(self, driver):
        citizen_page = go_to_citizen_page(driver)
        values = valid_values()
        values['gender'] = ''
        citizen_page.fill_citizen_page(**values)
        assert citizen_page.is_next_button_disabled()

    @pytest.mark.negative
    def test_fill_citizen_page_with_invalid_length_passport(self, driver):
        citizen_page = go_to_citizen_page(driver)
        values = valid_values()
        values['passport'] = 'А'
        citizen_page.fill_citizen_page(**values)
        assert citizen_page.is_next_button_disabled()

    def test_fill_citizen_page_with_space_passport(self,driver):
        citizen_page = go_to_citizen_page(driver)
        values = valid_values()
        values['passport'] = '         '
        citizen_page.fill_citizen_page(**values)
        assert citizen_page.is_next_button_disabled()

    def test_fill_citizen_page_with_digits_midname(self, driver):
        citizen_page = go_to_citizen_page(driver)
        values = valid_values()
        values['midname'] = 'Ivanovich123'
        citizen_page.fill_citizen_page(**values)
        assert citizen_page.is_next_button_disabled()


