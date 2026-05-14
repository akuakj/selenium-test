import pytest
from faker import Faker
import allure
from allure_commons.types import Severity
from UI.pages.home_page import HomePage
from UI.pages.applicant_page import ApplicantPage
from UI.pages.service_page import ServicePage
from UI.pages.citizen_page import CitizenPage
from UI.pages.marriage_page import MarriagePage
from logger import get_logger

fake = Faker('ru_RU')

@allure.feature("user flow регистрации брака")
class TestMarriageFlow:
# вынести
    def setup_method(self):
        self.logger = get_logger(__name__)

    @allure.title("Заполнение всех форм валидными данными")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_marriage_registration_full_flow(self, driver):

        with allure.step("Открыть главную страницу"):
            self.logger.info("Открытие главной страницы")
            home_page = HomePage(driver)
            home_page.open()
            home_page.click_login_as_user()

        with allure.step("Заполнить данные заявителя"):
            self.logger.info("Заполнение формы заявителя")
            applicant_page = ApplicantPage(driver)
            applicant_page.fill_applicant_page(
                surname=fake.last_name(),
                name=fake.first_name(),
                midname=fake.middle_name(),
                phone=fake.numerify('###########'),
                passport=fake.bothify('??######', letters='АВРСКЕОТН'),
                address=fake.address()
            )
            applicant_page.click_next()

        with allure.step("Выбрать услугу - Регистрация брака"):
            self.logger.info("Выбор услуги: Регистрация брака")
            ServicePage(driver).select_marriage()

        with allure.step("Заполнить данные гражданина"):
            self.logger.info("Заполнение формы гражданина")
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

        with allure.step("Заполнить данные брака"):
            self.logger.info("Заполнение формы брака")
            marriage_page = MarriagePage(driver)
            marriage_page.fill_marriage_page(
                marriage_date=fake.date_between().strftime('%d%m%Y'),
                new_surname=fake.last_name(),
                spouse_surname=fake.last_name(),
                spouse_name=fake.first_name(),
                spouse_midname=fake.middle_name(),
                spouse_birthdate=fake.date_of_birth(minimum_age=18).strftime('%d%m%Y'),
                spouse_passport=fake.bothify('??######', letters='АВРСКЕОТН')
            )
            status_page = marriage_page.click_finish()

        with allure.step("Проверить статус заявки"):
            self.logger.info("Проверка статуса заявки")
            status_page.check_status_displayed()
            status_page.check_success_message_displayed()