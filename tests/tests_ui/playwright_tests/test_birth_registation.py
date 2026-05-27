import allure
from allure_commons.types import Severity
from faker import Faker
from playwright.sync_api import sync_playwright
from UI.playwright_pages.home_page import HomePage
from UI.playwright_pages.applicant_page import ApplicantPage
from UI.playwright_pages.service_page import ServicePage
from UI.playwright_pages.citizen_page import CitizenPage
from UI.playwright_pages.birth_page import BirthPage
from UI.playwright_pages.status_page import StatusPage
from utils.logger import get_logger
from utils.enums import Gender, ServiceType


fake = Faker('ru_RU')
logger = get_logger(__name__)


@allure.epic("playwright ui")
@allure.feature("Регистрация рождения")
class TestBirthRegistration:

    @allure.title("Полный путь регистрации заявки рождения валидными данными")
    @allure.story("Позитивный сценарий")
    @allure.severity(Severity.CRITICAL)
    def test_birth_registration(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            try:
                with allure.step("Открыть главную страницу и войти как пользователь"):
                    logger.info("Открываем главную страницу")
                    home = HomePage(page)
                    home.open()
                    home.click_login_as_user()
                    logger.info("нажата кнопка 'войти как пользователь'")

                with allure.step('Заполнить данные заявителя'):
                    logger.info('Заполняем данные заявителя')
                    applicant = ApplicantPage(page)
                    applicant.fill_applicant(
                        surname=fake.last_name(),
                        name=fake.first_name(),
                        midname=fake.middle_name(),
                        phone=fake.numerify('########'),
                        passport=fake.bothify('??#####', letters='АВРСТ'),
                        address=fake.street_address()
                    )
                    applicant.click_next()
                    logger.info('Данные заявителя заполнены, нажата кнопка "Далее"')

                with allure.step(f"Выбрать услугу: {ServiceType.BIRTH.value}"):
                    logger.info(f"Выбираем услугу: {ServiceType.BIRTH.value}")
                    service = ServicePage(page)
                    service.select_birth()
                    logger.info("Услуга выбрана")

                with allure.step("Заполнить данные гражданина"):
                    citizen = CitizenPage(page)
                    citizen.fill_citizen(
                        surname=fake.last_name(),
                        name=fake.first_name(),
                        midname=fake.middle_name(),
                        birth=fake.date_of_birth(minimum_age=16).strftime('%Y-%m-%d'),
                        passport=fake.bothify('??#####', letters='АВРОНСТ'),
                        gender=Gender.MALE_FULL.value,
                        address=fake.street_address()
                    )
                    citizen.click_next()
                    logger.info("Данные гражданина заполнены, нажата кнопка Далее")

                with allure.step("Заполнить данные услуги — рождение"):

                    birth = BirthPage(page)
                    birth.fill_birth(
                        place=fake.street_address(),
                        mother=fake.first_name_female(),
                        father=fake.first_name_male(),
                        granny=fake.first_name_female(),
                        granddad=fake.first_name_male()
                    )
                    birth.click_finish()
                    logger.info("Данные услуги заполнены, нажата кнопка Завершить")

                with allure.step("Проверить финальный экран"):
                    status = StatusPage(page)

                with allure.step("Проверить текст 'Спасибо за обращение!'"):
                    logger.info("Проверяем текст благодарности")
                    assert status.get_thx_text().is_visible(), \
                        "Текст 'Спасибо за обращение!' не отображается"
                    logger.info("Текст 'Спасибо за обращение!' отображается")

                with allure.step("Проверить статус заявки"):
                    logger.info("Проверяем статус заявки")
                    assert status.get_status_text().is_visible(), \
                        "Текст 'отправлена на рассмотрение' не отображается"
                    logger.info("Статус заявки отображается корректно")

            except AssertionError as e:
                logger.error(f"Тест упал на проверке: {e}")
                raise

            except Exception as e:
                logger.error(f"Неожиданная ошибка: {e}")
                raise

            finally:
                logger.info("Закрываем браузер")
                browser.close()

test = TestBirthRegistration()
test.test_birth_registration()