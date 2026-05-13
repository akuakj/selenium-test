import pytest
from faker import Faker

fake = Faker('ru_RU')

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

    @pytest.mark.positive
    def test_fill_citizen_page_with_all_valid_values(self, driver, citizen_page_ready):
        values = valid_values()
        citizen_page_ready.fill_citizen_page(**values)
        citizen_page_ready.check_next_button_enabled()

    @pytest.mark.negative
    def test_fill_citizen_page_without_surname(self, driver, citizen_page_ready):
        values = valid_values()
        values['surname'] = ''
        citizen_page_ready.fill_citizen_page(**values)
        citizen_page_ready.check_next_button_disabled()

    @pytest.mark.negative
    def test_fill_citizen_page_with_future_birthdate(self, driver, citizen_page_ready):
        values = valid_values()
        values['birthdate'] = '10.03.3036'
        citizen_page_ready.fill_citizen_page(**values)
        citizen_page_ready.check_next_button_disabled()

    @pytest.mark.negative
    def test_fill_citizen_page_without_gender(self, driver, citizen_page_ready):
        values = valid_values()
        values['gender'] = ''
        citizen_page_ready.fill_citizen_page(**values)
        citizen_page_ready.check_next_button_disabled()

    @pytest.mark.negative
    def test_fill_citizen_page_with_invalid_length_passport(self, driver, citizen_page_ready):
        values = valid_values()
        values['passport'] = 'А'
        citizen_page_ready.fill_citizen_page(**values)
        citizen_page_ready.check_next_button_disabled()

    @pytest.mark.negative
    def test_fill_citizen_page_with_space_passport(self,driver, citizen_page_ready):
        values = valid_values()
        values['passport'] = '         '
        citizen_page_ready.fill_citizen_page(**values)
        citizen_page_ready.check_next_button_disabled()

    @pytest.mark.negative
    def test_fill_citizen_page_with_digits_midname(self, driver, citizen_page_ready):
        values = valid_values()
        values['midname'] = 'Ivanovich123'
        citizen_page_ready.fill_citizen_page(**values)
        citizen_page_ready.check_next_button_disabled()