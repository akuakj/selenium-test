import pytest
from pages.applicant_page import ApplicantPage
from pages.home_page import HomePage
from faker import Faker

fake = Faker('ru_RU')

def valid_values():
    return dict(
        surname=fake.last_name(),
        name=fake.first_name(),
        midname=fake.middle_name(),
        phone=fake.numerify('###########'),
        passport=fake.bothify('??######', letters='АВРСКЕОТН'),
        address=fake.address()
    )

def go_to_applicant_page(driver):
    HomePage(driver).open()
    HomePage(driver).click_login_as_user()
    return ApplicantPage(driver)


class TestApplicantPage:

    @pytest.mark.positive
    def test_fill_applicant_page_with_all_valid_values(self, driver):
        applicant_page = go_to_applicant_page(driver)
        values = valid_values()
        applicant_page.fill_applicant_page(**values)
        assert applicant_page.is_next_button_enabled()

    @pytest.mark.negative
    def test_fill_applicant_page_with_invalid_length_midname(self, driver):
        applicant_page = go_to_applicant_page(driver)
        values = valid_values()
        values['midname'] = 'test'
        applicant_page.fill_applicant_page(**values)
        assert applicant_page.is_next_button_disabled()

    @pytest.mark.xfail(reason="баг: пробелы проходят валидацию отчества")
    def test_fill_applicant_page_with_space(self, driver):
        applicant_page = go_to_applicant_page(driver)
        values = valid_values()
        values['midname'] = '      '
        applicant_page.fill_applicant_page(**values)
        assert applicant_page.is_next_button_disabled()

    @pytest.mark.positive
    def test_fill_applicant_page_without_surname(self, driver):
        applicant_page = go_to_applicant_page(driver)
        values = valid_values()
        values['surname'] = ''
        applicant_page.fill_applicant_page(**values)

        assert applicant_page.is_next_button_disabled()


