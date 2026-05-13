import pytest
from faker import Faker

fake = Faker('ru_RU')


class TestBirthFlow:

    @pytest.mark.positive
    def test_birth_registration_full_flow(self, driver, birth_page_ready):
        birth_page_ready.fill_birth_page(
            place_of_birth=fake.address(),
            mother=' '.join([fake.first_name_female(), fake.last_name_female(), fake.middle_name_female()]),
            father=' '.join([fake.first_name_male(), fake.last_name_male(), fake.middle_name_male()]),
            granny=' '.join([fake.first_name_female(), fake.last_name_female(), fake.middle_name_female()]),
            grandad=' '.join([fake.first_name_male(), fake.last_name_male(), fake.middle_name_male()])
        )
        status_page = birth_page_ready.click_finish()
        status_page.check_status_displayed()
        status_page.check_success_message_displayed()