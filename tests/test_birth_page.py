import time

import pytest
from pages.home_page import HomePage
from pages.applicant_page import ApplicantPage
from pages.service_page import ServicePage
from pages.citizen_page import CitizenPage
from pages.birth_page import BirthPage
from faker import Faker

fake = Faker('ru_RU')

def valid_value():
    return dict (
        place_of_birth = fake.address(),
        mother = ' '.join([fake.first_name_female(), fake.last_name_female(), fake.middle_name_female()]),
        father = ' '.join([fake.first_name_male(), fake.last_name_male(), fake.middle_name_male()]),
        granny = ' '.join([fake.first_name_female(), fake.last_name_female(), fake.middle_name_female()]),
        grandad = ' '.join([fake.first_name_male(), fake.last_name_male(), fake.middle_name_male()])
    )

def go_to_birth_page(driver):
    HomePage(driver).open()
    HomePage(driver).click_login_as_user()

    applicant_page = ApplicantPage(driver)
    applicant_page.fill_applicant_page(
        surname = fake.last_name(),
        name = fake.first_name(),
        midname = fake.middle_name(),
        phone = fake.numerify('#########'),
        passport = fake.bothify('??######', letters='АВРОСТНК'),
        address = fake.address()
    )
    applicant_page.click_next()

    ServicePage(driver).select_birth()

    citizen_page = CitizenPage(driver)
    citizen_page.fill_citizen_page(
        surname=fake.last_name(),
        name=fake.first_name(),
        midname=fake.middle_name(),
        birthdate=fake.date_of_birth(minimum_age=16).strftime('%d.%m.%Y'),
        passport=fake.bothify('??######', letters='АВРОНТСК'),
        gender=fake.random_element(['муж', 'жен', 'м', 'ж']),
        address=fake.address()
    )
    citizen_page.click_next()

    return BirthPage(driver)

class TestBirthPage:
    def test_fill_birth_page_all_valid_values(self, driver):
        birth_page = go_to_birth_page(driver)
        values = valid_value()
        birth_page.fill_birth_page(**values)
        time.sleep(10)
        assert birth_page.is_finish_button_enabled()

    @pytest.mark.negative
    def test_fill_birth_page_invalid_symbols_father(self,driver):
        birth_page = go_to_birth_page(driver)
        values = valid_value()
        values['father'] = '34323223123123'
        birth_page.fill_birth_page(**values)
        assert birth_page.is_finish_button_disabled()

    def test_fill_birth_page_without_grandad(self, driver):
        birth_page = go_to_birth_page(driver)
        values = valid_value()
        values['grandad'] = ''
        birth_page.fill_birth_page(**values)
        assert birth_page.is_finish_button_disabled()

    @pytest.mark.negative
    def test_fill_birth_page_with_invalid_length_father(self, driver):
        birth_page = go_to_birth_page(driver)
        values = valid_value()
        values['father'] = 'аа'
        birth_page.fill_birth_page(**values)
        assert birth_page.is_finish_button_disabled()
