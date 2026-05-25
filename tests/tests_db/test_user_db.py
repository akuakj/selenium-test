import allure
import pytest
from allure_commons.types import Severity
from faker import Faker
from API.models.user_models import UserResponse
from API.data.user_data import get_valid_marriage_payload, get_valid_birth_payload
from utils.enums import StatusOfApplicationAPI
from utils.logger import get_logger

fake = Faker('ru_RU')
logger = get_logger(__name__)


@allure.epic("API + DB")
@allure.feature("Проверка данных заявителей в БД")
class TestApplicantDB:

    @allure.title("POST /sendUserRequest (брак) — заявитель сохраняется в БД")
    @allure.story("Данные заявителя")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_marriage_applicant_saved_in_db(self, user_api, db):

        with allure.step("Подготовить payload с фиксированным паспортом"):
            passport = fake.bothify('??#####', letters='АВРОНСТ')
            payload = get_valid_marriage_payload(personalNumberOfPassport=passport)
            logger.info(f"Паспорт заявителя: {passport}")

        with allure.step("POST /sendUserRequest — отправить заявку на брак"):
            response = user_api.send_user_request(payload)
            logger.info(f"Response {response.status_code}: {response.json()}")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("Получить applicantid из ответа API"):
            parsed = UserResponse(**response.json())
            applicant_id = parsed.data.applicantid
            logger.info(f"applicantid: {applicant_id}")
            assert applicant_id > 0

        with allure.step("Запросить заявителя из БД по applicantid"):
            applicant = db.get_applicant_by_id(applicant_id)
            logger.info(f"Запись из БД: {applicant}")

        with allure.step("Проверить что запись существует в БД"):
            assert applicant, (
                f"Заявитель с applicantid={applicant_id} не найден в БД"
            )

        with allure.step("Проверить что паспорт в БД совпадает с отправленным"):
            assert applicant.passportnumber == passport, (
                f"Паспорт в БД: '{applicant.passportnumber}', ожидался: '{passport}'"
            )

        with allure.step("Проверить что фамилия заявителя не пустая"):
            assert applicant.surname, "Поле surname в БД пустое"

        with allure.step("Проверить что имя заявителя не пустое"):
            assert applicant.name, "Поле name в БД пустое"

        with allure.step("Проверить что отчество заявителя не пустое"):
            assert applicant.middlename, "Поле middlename в БД пустое"

        with allure.step("Проверить что телефон заявителя не пустой"):
            assert applicant.phonenumber, "Поле phonenumber в БД пустое"

    @allure.title("POST /sendUserRequest (брак) — заявка сохраняется в БД с корректными данными")
    @allure.story("Данные заявки")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_marriage_application_saved_in_db(self, user_api, db):

        with allure.step("Подготовить и отправить заявку на брак"):
            response = user_api.send_user_request(get_valid_marriage_payload())
            logger.info(f"Response {response.status_code}: {response.json()}")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("Получить applicationid и citizenid из ответа API"):
            parsed = UserResponse(**response.json())
            application_id = parsed.data.applicationid
            citizen_id = parsed.data.citizenid
            logger.info(f"applicationid: {application_id}, citizenid: {citizen_id}")
            assert application_id > 0
            assert citizen_id > 0

        with allure.step("Запросить заявку из БД по applicationid"):
            application = db.get_application_by_id(application_id)
            logger.info(f"Запись из БД: {application}")

        with allure.step("Проверить что заявка существует в БД"):
            assert application is not None, (
                f"Заявка с applicationid={application_id} не найдена в БД"
            )

        with allure.step("Проверить что тип заявки корректный"):
            logger.info(f"Тип заявки: {application.kindofapplication}")
            assert application.kindofapplication == "Получение свидетельства о браке", (
                f"Ожидался тип 'Получение свидетельства о браке', получен '{application.kindofapplication}'"
            )

        with allure.step("Проверить что статус заявки после создания — under consideration"):
            logger.info(f"Статус заявки: {application.statusofapplication}")
            assert application.statusofapplication == StatusOfApplicationAPI.UNDER_CONSIDERATION.value, (
                f"Ожидался статус '{StatusOfApplicationAPI.UNDER_CONSIDERATION.value}', "
                f"получен '{application.statusofapplication}'"
            )

        with allure.step("Проверить что citizenid в заявке совпадает с ответом API"):
            assert application.citizenid == citizen_id, (
                f"citizenid в БД: {application.citizenid}, ожидался: {citizen_id}"
            )

        with allure.step("Проверить что staffid пустой — заявка ещё не обработана"):
            logger.info(f"staffid: {application.staffid}")
            assert application.staffid is None, (
                f"staffid должен быть None, получен {application.staffid}"
            )

    @allure.title("POST /sendUserRequest (брак) — гражданин сохраняется в БД с корректными данными")
    @allure.story("Данные гражданина")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_marriage_citizen_saved_in_db(self, user_api, db):

        with allure.step("Подготовить payload с фиксированными данными гражданина"):
            citizen_passport = fake.bothify('??#####', letters='АВРОНСТ')
            payload = get_valid_marriage_payload(citizenNumberOfPassport=citizen_passport)
            logger.info(f"Паспорт гражданина: {citizen_passport}")

        with allure.step("POST /sendUserRequest — отправить заявку на брак"):
            response = user_api.send_user_request(payload)
            logger.info(f"Response {response.status_code}: {response.json()}")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("Получить citizenid из ответа API"):
            parsed = UserResponse(**response.json())
            citizen_id = parsed.data.citizenid
            logger.info(f"citizenid: {citizen_id}")
            assert citizen_id > 0

        with allure.step("Запросить гражданина из БД по citizenid"):
            citizen = db.get_citizen_by_id(citizen_id)
            logger.info(f"Запись из БД: {citizen}")

        with allure.step("Проверить что запись существует в БД"):
            assert citizen is not None, (
                f"Гражданин с citizenid={citizen_id} не найден в БД"
            )

        with allure.step("Проверить что паспорт гражданина совпадает с отправленным"):
            assert citizen.passportnumber == citizen_passport, (
                f"Паспорт в БД: '{citizen.passportnumber}', ожидался: '{citizen_passport}'"
            )

        with allure.step("Проверить что фамилия гражданина не пустая"):
            assert citizen.surname, "Поле surname гражданина в БД пустое"

        with allure.step("Проверить что пол гражданина не пустой"):
            logger.info(f"Пол гражданина: {citizen.gender}")
            assert citizen.gender, "Поле gender гражданина в БД пустое"

        with allure.step("Проверить что дата рождения гражданина не пустая"):
            logger.info(f"Дата рождения: {citizen.dateofbirth}")
            assert citizen.dateofbirth, "Поле dateofbirth гражданина в БД пустое"

    @allure.title("POST /sendUserRequest (рождение) — заявитель сохраняется в БД")
    @allure.story("Данные заявителя")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_birth_applicant_saved_in_db(self, user_api, db):

        with allure.step("Подготовить payload с фиксированным паспортом"):
            passport = fake.bothify('??#####', letters='АВРОНСТ')
            payload = get_valid_birth_payload(personalNumberOfPassport=passport)
            logger.info(f"Паспорт заявителя: {passport}")

        with allure.step("POST /sendUserRequest — отправить заявку на рождение"):
            response = user_api.send_user_request(payload)
            logger.info(f"Response {response.status_code}: {response.json()}")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("Получить applicantid из ответа API"):
            parsed = UserResponse(**response.json())
            applicant_id = parsed.data.applicantid
            logger.info(f"applicantid: {applicant_id}")
            assert applicant_id > 0

        with allure.step("Запросить заявителя из БД по applicantid"):
            applicant = db.get_applicant_by_id(applicant_id)
            logger.info(f"Запись из БД: {applicant}")

        with allure.step("Проверить что запись существует в БД"):
            assert applicant is not None, (
                f"Заявитель с applicantid={applicant_id} не найден в БД"
            )

        with allure.step("Проверить что паспорт в БД совпадает с отправленным"):
            assert applicant.passportnumber == passport, (
                f"Паспорт в БД: '{applicant.passportnumber}', ожидался: '{passport}'"
            )

    @allure.title("POST /sendUserRequest (рождение) — свидетельство о рождении сохраняется в БД")
    @allure.story("Свидетельство о рождении")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_birth_certificate_saved_in_db(self, user_api, db):

        with allure.step("Подготовить payload с фиксированными данными"):
            birth_place = fake.street_address()
            birth_mother = fake.first_name()
            payload = get_valid_birth_payload(
                birth_place=birth_place,
                birth_mother=birth_mother
            )
            logger.info(f"Место рождения: {birth_place}, мать: {birth_mother}")

        with allure.step("POST /sendUserRequest — отправить заявку на рождение"):
            response = user_api.send_user_request(payload)
            logger.info(f"Response {response.status_code}: {response.json()}")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("Получить citizenid из ответа API"):
            parsed = UserResponse(**response.json())
            citizen_id = parsed.data.citizenid
            logger.info(f"citizenid: {citizen_id}")
            assert citizen_id > 0

        with allure.step("Запросить свидетельство о рождении из БД по citizenid"):
            certificate = db.get_birth_certificate_by_citizen_id(citizen_id)
            logger.info(f"Запись из БД: {certificate}")

        with allure.step("Проверить что свидетельство существует в БД"):
            assert certificate is not None, (
                f"Свидетельство для citizenid={citizen_id} не найдено в БД"
            )

        with allure.step("Проверить что место рождения совпадает с отправленным"):
            logger.info(f"Место рождения в БД: {certificate.placeofbirth}")
            assert certificate.placeofbirth == birth_place, (
                f"Место рождения в БД: '{certificate.placeofbirth}', ожидалось: '{birth_place}'"
            )

        with allure.step("Проверить что имя матери совпадает с отправленным"):
            logger.info(f"Мать в БД: {certificate.mother}")
            assert certificate.mother == birth_mother, (
                f"Мать в БД: '{certificate.mother}', ожидалась: '{birth_mother}'"
            )

        with allure.step("Проверить что имя отца не пустое"):
            assert certificate.father, "Поле father в свидетельстве пустое"

    @allure.title("POST /sendUserRequest (рождение) — заявка сохраняется со статусом under consideration")
    @allure.story("Данные заявки")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.positive
    def test_birth_application_initial_status_in_db(self, user_api, db):

        with allure.step("Отправить заявку на рождение"):
            response = user_api.send_user_request(get_valid_birth_payload())
            logger.info(f"Response {response.status_code}: {response.json()}")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("Получить applicationid из ответа API"):
            parsed = UserResponse(**response.json())
            application_id = parsed.data.applicationid
            logger.info(f"applicationid: {application_id}")
            assert application_id > 0

        with allure.step("Запросить статус заявки из БД"):
            status = db.get_application_status(application_id)
            logger.info(f"Начальный статус в БД: {status}")

        with allure.step("Проверить что начальный статус — under consideration"):
            assert status == StatusOfApplicationAPI.UNDER_CONSIDERATION.value, (
                f"Ожидался статус '{StatusOfApplicationAPI.UNDER_CONSIDERATION.value}', получен '{status}'"
            )