import pytest
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

class TestBirthPage:

    @pytest.mark.positive
    def test_fill_birth_page_all_valid_values(self, driver, birth_page_ready):
        values = valid_value()
        birth_page_ready.fill_birth_page(**values)
        assert birth_page_ready.is_finish_button_enabled()

    @pytest.mark.negative
    def test_fill_birth_page_invalid_symbols_father(self,driver, birth_page_ready):
        values = valid_value()
        values['father'] = '34323223123123'
        birth_page_ready.fill_birth_page(**values)
        assert birth_page_ready.is_finish_button_disabled()

    @pytest.mark.negative
    def test_fill_birth_page_without_grandad(self, driver, birth_page_ready):
        values = valid_value()
        values['grandad'] = ''
        birth_page_ready.fill_birth_page(**values)
        assert birth_page_ready.is_finish_button_disabled()

    @pytest.mark.negative
    def test_fill_birth_page_with_invalid_length_father(self, driver, birth_page_ready):
        values = valid_value()
        values['father'] = 'аа'
        birth_page_ready.fill_birth_page(**values)
        assert birth_page_ready.is_finish_button_disabled()
