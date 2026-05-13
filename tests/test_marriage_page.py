import pytest
from faker import Faker
import allure
from allure_commons.types import Severity

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
@allure.feature("Данные брака")
class TestMarriagePage:

    @allure.title("Заполнение всех полей валидными данными")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_fill_marriage_page_all_valid_values(self, driver, marriage_page_ready):
        values = valid_value()
        marriage_page_ready.fill_marriage_page(**values)
        marriage_page_ready.check_finish_button_enabled()

    @allure.title("Недопустимые символы в поле новой фамилии")
    @allure.story("Негативные сценарии")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_fill_marriage_page_invalid_symbols_newsurname(self,driver, marriage_page_ready):
        values = valid_value()
        values['new_surname'] = '##!ащлвыа'
        marriage_page_ready.fill_marriage_page(**values)
        marriage_page_ready.check_finish_button_disabled()

    @allure.title("Пустое значение в поле паспорт супруга")
    @allure.story("Негативные сценарии")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_fill_marriage_page_without_spouse_passport(self, driver, marriage_page_ready):
        values = valid_value()
        values['spouse_passport'] = ''
        marriage_page_ready.fill_marriage_page(**values)
        marriage_page_ready.check_finish_button_disabled()

    @allure.title("Максимальная длина значения в поле Фамилия - 20 символов")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.positive
    def test_fill_marriage_page_with_max_length_spouse_name(self, driver, marriage_page_ready):
        values = valid_value()
        values['spouse_name'] = str('a' * 20)
        marriage_page_ready.fill_marriage_page(**values)
        marriage_page_ready.check_finish_button_enabled()
