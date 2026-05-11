import pytest
from pages.home_page import HomePage
from pages.applicant_page import ApplicantPage
from pages.service_page import ServicePage
from pages.citizen_page import CitizenPage
from pages.marriage_page import MarriagePage
from faker import Faker

fake = Faker('ru_RU')

def valid_value():
    return dict (
        marriage_date = fake.date_object().strftime('%d.%m.%Y'),
        new_surname = fake.last_name(),
        spouce_surname = fake.last_name(),
        spouce_name = fake.name(),
        spouce_midname = fake.middle_name(),
        spouce_birthdate = fake.date_of_birth(minimum_age=16).strftime('%d.%m.%Y'),
        spouce_passport = fake.bothify('??######', letters = 'АВРСКНОТ'),
    )

def go_to_marriage_page(driver):
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

    ServicePage(driver).select_marriage()

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

    return MarriagePage(driver)

class TestMarriagePage:
    def test_fill_marriage_page_all_valid_values(self, driver):
        marriage_page = go_to_marriage_page(driver)
        values = valid_value()
        marriage_page.fill_marriage_page(**values)
        assert marriage_page.is_finish_button_enabled()

    @pytest.mark.negative
    def test_fill_marriage_page_invalid_symbols_newsurname(self,driver):
        marriage_page = go_to_marriage_page(driver)
        values = valid_value()
        values['new_surname'] = '##!ащлвыа'
        marriage_page.fill_marriage_page(**values)
        assert marriage_page.is_finish_button_disabled()

    def test_fill_marriage_page_without_spouse_passport(self, driver):
        marriage_page = go_to_marriage_page(driver)
        values = valid_value()
        values['spouse_passport'] = ''
        marriage_page.fill_marriage_page(**values)
        assert marriage_page.is_finish_button_disabled()

    @pytest.mark.negative
    def test_fill_marriage_page_with_invalid_length_spouse_name(self, driver):
        marriage_page = go_to_marriage_page(driver)
        values = valid_value()
        values['spouse_name'] = str('a' * 50)
        marriage_page.fill_marriage_page(**values)
        assert marriage_page.is_finish_button_disabled()
