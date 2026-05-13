import pytest
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

class TestApplicantPage:
    @pytest.mark.positive
    def test_fill_applicant_page_with_all_valid_values(self, driver, applicant_page_ready_user):
        values = valid_values()
        applicant_page_ready_user.fill_applicant_page(**values)
        applicant_page_ready_user.check_next_button_enabled()

    @pytest.mark.negative
    def test_fill_applicant_page_with_invalid_length_midname(self, driver, applicant_page_ready_user):
        values = valid_values()
        values['midname'] = 'test'
        applicant_page_ready_user.fill_applicant_page(**values)
        applicant_page_ready_user.check_next_button_disabled()

    @pytest.mark.xfail(reason="баг: пробел\ы проходят валидацию отчества")
    def test_fill_applicant_page_with_space(self, driver, applicant_page_ready_user):
        values = valid_values()
        values['midname'] = '      '
        applicant_page_ready_user.fill_applicant_page(**values)
        applicant_page_ready_user.check_next_button_disabled()

    @pytest.mark.negative
    def test_fill_applicant_page_without_surname(self, driver, applicant_page_ready_user):
        values = valid_values()
        values['surname'] = ''
        applicant_page_ready_user.fill_applicant_page(**values)
        applicant_page_ready_user.check_next_button_disabled()