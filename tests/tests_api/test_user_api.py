import allure
import pytest
from allure_commons.types import Severity
from api.models.user_models import UserResponse, UserBadRequest
from tests.conftest import db_client
from utils.logger import get_logger
from api.data.user_data import get_valid_marriage_payload, get_valid_birth_payload
from utils.enums import Mode

logger = get_logger(__name__)


@allure.epic("api")
@allure.feature("Тестирование user-запросов")
class TestUserAPI:

    @allure.title("POST /sendUserRequest - регистрация брака, валидные данные - 200")
    @allure.story("Услуга регистрации брака")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_send_marriage_request_returns_200(self, user_api, db_client):

        with allure.step("Подготовить валидные данные для регистрации брака"):
            payload = get_valid_marriage_payload()
            logger.info(f"Payload: {payload.model_dump()}")

        with allure.step("отправить валидный запрос на регистрацию брака"):
            response = user_api.send_user_request(payload)
            logger.info(f"Response body: {response.json()}")

        with allure.step("проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("проверить структуру ответа с Pydantic-моделью"):
            user_body_response = UserResponse(**response.json())

        with allure.step("проверить, что в ответе присутствует поле merrigecertificateid"):
            assert hasattr(user_body_response.data, "merrigecertificateid"), "Поле отсутствует в ответе"

        with allure.step("Получить данные заявки из БД"):
            db_application = db_client.get_application_by_id(user_body_response.data.applicationid)

        with allure.step("проверить данные ответа с данными в БД"):
            assert user_body_response.data.applicantid == db_application.applicantid
            assert user_body_response.data.citizenid == db_application.citizenid

        with allure.step("проверить данные запроса с данными в БД"):
            assert payload.mode == Mode.WEDDING.value

            db_applicant = db_client.get_applicant_by_id(db_application.applicantid)
            assert payload.personalFirstName == db_applicant.name
            assert payload.personalPhoneNumber == db_applicant.phonenumber
            assert payload.personalAddress == db_applicant.registration_address

            db_citizen = db_client.get_citizen_by_id(db_application.citizenid)
            assert payload.citizenNumberOfPassport == db_citizen.passportnumber
            assert payload.citizenMiddleName == db_citizen.middlename

    @allure.title("POST /sendUserRequest - регистрация рождения, валидные данные - 200")
    @allure.story("Услуга регистрации рождения")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_send_birth_request_returns_200(self, user_api, db_client):

        with allure.step("Подготовить валидные данные для регистрации рождения"):
            payload = get_valid_birth_payload()
            logger.info(f"Payload: {payload.model_dump()}")

        with allure.step("отправить валидный запрос на регистрацию рождения"):
            response = user_api.send_user_request(payload)
            logger.info(f"response body: {response.json()}")

        with allure.step("проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("проверить структуру ответа с Pydantic-моделью"):
            user_body_response = UserResponse(**response.json())

        with allure.step("в ответе присутсвует поле birthcertificateid"):
            assert hasattr(user_body_response.data, "birthcertificateid"), "Поле отсутствует в ответе"

        with allure.step("Получить данные заявки из БД"):
            db_application = db_client.get_application_by_id(user_body_response.data.applicationid)

        with allure.step("проверить данные ответа с данными в БД"):
            assert user_body_response.data.applicantid == db_application.applicantid
            assert user_body_response.data.citizenid == db_application.citizenid

        with allure.step("проверить данные запроса с данными в БД"):
            db_applicant = db_client.get_applicant_by_id(db_application.applicantid)
            assert payload.personalFirstName == db_applicant.name
            assert payload.personalPhoneNumber == str(db_applicant.phonenumber)
            assert payload.personalAddress == db_applicant.registration_address

            db_citizen = db_client.get_citizen_by_id(db_application.citizenid)
            assert payload.citizenFirstName == db_citizen.name
            assert payload.citizenMiddleName == db_citizen.middlename
            assert payload.citizenNumberOfPassport == db_citizen.passportnumber

    @allure.title("POST /sendUserRequest — пустой паспорт заявителя -> 400")
    @allure.story("Услуга регистрации брака")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_send_marriage_request_without_passport_returns_error(self, user_api):

        with allure.step("Подготовить данные с пустым паспортом"):
            payload = get_valid_marriage_payload(personalNumberOfPassport=None)

        with allure.step("Отправить запрос"):
            response = user_api.send_user_request(payload)
            logger.info(f"Response body: {response.text}")

        with allure.step("Проверить что статус код 400"):
            assert response.status_code == 400, (
                f"Ожидался 400, получен {response.status_code}"
            )

        with allure.step("Проверить структуру ответа ошибки через Pydantic-модель"):
            error = UserBadRequest(**response.json())
            assert hasattr(error, "code") and hasattr(error, "message")

    @allure.title("POST /sendUserRequest — пустое значение в поле места рождения -> 400")
    @allure.story("Услуга регистрации рождения")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_send_birth_request_without_birthplace_returns_error(self, user_api):

        with allure.step("Подготовить данные с пустым паспортом"):
            payload = get_valid_birth_payload(birth_place=None)

        with allure.step("Отправить запрос"):
            response = user_api.send_user_request(payload)
            logger.info(f"Response body: {response.text}")

        with allure.step("Проверить что статус код 400"):
            assert response.status_code == 400, (
                f"Ожидался код ошибки, получен {response.status_code}"
            )

        with allure.step("Проверить структуру ответа ошибки через Pydantic-модель"):
            error = UserBadRequest(**response.json())
            assert hasattr(error, "code") and hasattr(error, "message")
