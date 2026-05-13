import pytest
from faker import Faker

fake = Faker('ru_RU')

def valid_values():
    return dict(
        surname = fake.last_name(),
        name = fake.first_name(),
        midname = fake.middle_name(),
        phone = fake.numerify('#########'),
        passport = fake.bothify('??#######', letters = 'АВРСКЕОНТ'),
        birthdate = fake.date_of_birth(minimum_age=18).strftime('%d.%m.%Y')
    )

class TestAdminRegistrationPage:

    @pytest.mark.positive
    def test_fill_all_valid_values(self, driver, admin_page_ready):
        values = valid_values()
        admin_page_ready.fill_admin_page(**values)
        admin_page_ready.check_next_button_enabled()

    @pytest.mark.negative
    def test_fill_admin_page_without_surname(self, driver, admin_page_ready):
        values = valid_values()
        values['surname'] = ''
        admin_page_ready.fill_admin_page(**values)
        admin_page_ready.check_next_button_disabled()


    @pytest.mark.negative
    def test_fill_admin_page_with_future_birthdate(self, driver, admin_page_ready):
        values = valid_values()
        values['birthdate'] = '01.01.3000'
        admin_page_ready.fill_admin_page(**values)
        admin_page_ready.check_next_button_disabled()

    @pytest.mark.negative
    def test_fill_admin_page_with_space_on_name(self, driver, admin_page_ready):
        values = valid_values()
        values['name'] = '      '
        admin_page_ready.fill_admin_page(**values)
        admin_page_ready.check_next_button_disabled()


    @pytest.mark.negative
    def test_fill_admin_page_invalid_length_passport(self, driver, admin_page_ready):
        values = valid_values()
        values['passport'] = 'А'
        admin_page_ready.fill_admin_page(**values)
        admin_page_ready.check_next_button_disabled()