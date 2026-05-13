import pytest
from faker import Faker
fake = Faker('ru_RU')


class TestMarriageFlow:

    @pytest.mark.positive
    def test_marriage_registration_full_flow(self, driver, marriage_page_ready):
        marriage_page_ready.fill_marriage_page(
            marriage_date=fake.date_between().strftime('%d%m%Y'),
            new_surname=fake.last_name(),
            spouse_surname=fake.last_name(),
            spouse_name=fake.first_name(),
            spouse_midname=fake.middle_name(),
            spouse_birthdate=fake.date_of_birth(minimum_age=18).strftime('%d%m%Y'),
            spouse_passport=fake.bothify('??######', letters='АВРСКЕОТН')
        )
        status_page = marriage_page_ready.click_finish()
        status_page.check_status_displayed()
        status_page.check_success_message_displayed()