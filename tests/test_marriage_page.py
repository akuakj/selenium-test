import pytest
from faker import Faker

fake = Faker('ru_RU')

def valid_value():
    return dict (
        marriage_date = fake.date_object().strftime('%d.%m.%Y'),
        new_surname = fake.last_name(),
        spouse_surname = fake.last_name(),
        spouse_name = fake.name(),
        spouse_midname = fake.middle_name(),
        spouse_birthdate = fake.date_of_birth(minimum_age=16).strftime('%d.%m.%Y'),
        spouse_passport = fake.bothify('??######', letters = 'АВРСКНОТ'),
    )

class TestMarriagePage:

    @pytest.mark.positive
    def test_fill_marriage_page_all_valid_values(self, driver, marriage_page_ready):
        values = valid_value()
        marriage_page_ready.fill_marriage_page(**values)
        marriage_page_ready.check_finish_button_enabled()

    @pytest.mark.negative
    def test_fill_marriage_page_invalid_symbols_newsurname(self,driver, marriage_page_ready):
        values = valid_value()
        values['new_surname'] = '##!ащлвыа'
        marriage_page_ready.fill_marriage_page(**values)
        marriage_page_ready.check_finish_button_disabled()

    @pytest.mark.negative
    def test_fill_marriage_page_without_spouse_passport(self, driver, marriage_page_ready):
        values = valid_value()
        values['spouse_passport'] = ''
        marriage_page_ready.fill_marriage_page(**values)
        marriage_page_ready.check_finish_button_disabled()

    @pytest.mark.positive
    def test_fill_marriage_page_with_max_length_spouse_name(self, driver, marriage_page_ready):
        values = valid_value()
        values['spouse_name'] = str('a' * 20)
        marriage_page_ready.fill_marriage_page(**values)
        marriage_page_ready.check_finish_button_enabled()
