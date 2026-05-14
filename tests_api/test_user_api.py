import allure
import pytest
from allure_commons.types import Severity
from api.models.user_models import UserResponse
from api.models.user_models import UserBadRequest
from logger import get_logger
from tests_api.conftest import user_api

logger = get_logger(__name__)

@allure.feature("Создание заявки пользователя")
class TestUserAPI:

    @allure.title("POST /sendUserRequest - регистрация брака, валидные данные - 200")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_send_marriage_request_returns_200(self, user_api, valid_marriage_payload):

        with allure.step("отправить валидный запрос на регистрацию брака"):
            response = user_api.send_user_request(valid_marriage_payload)
            logger.info(f"Response body: {response.json()}")

        with allure.step("проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("проверить структуру ответа с пайдантик моделью"):
            parsed = UserResponse(**response.json())

        with allure.step("проверить что id заявки больше 0"):
            assert parsed.data.applicationid > 0

        with allure.step("в ответе присутсвует поле merrigecertificateid"):
            assert hasattr(parsed.data, "merrigecertificateid"), "Поле отсутствует в ответе"

    @allure.title("POST /sendUserRequest - регистрация рождения, валидные данные - 200")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_send_birth_request_returns_200(self, user_api, valid_birth_payload):
        with allure.step("отправить валидный запрос на регистрацию рождения"):
            response = user_api.send_user_request(valid_birth_payload)
            logger.info(f"response body: {response.json()}")

        with allure.step("проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("проверить структуру ответа с пайдантик моделью"):
            parsed = UserResponse(**response.json())

        with allure.step("проверить что id заявки больше 0"):
            assert parsed.data.applicationid > 0

        with allure.step("в ответе присутсвует поле birthcertificateid"):
            assert hasattr(parsed.data, "birthcertificateid"), "Поле отсутствует в ответе"

    @allure.title("POST /sendUserRequest — пустой паспорт заявителя → не 200")
    @allure.story("Негативные сценарии")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_send_request_without_passport_returns_error(self, user_api, valid_marriage_payload):
        with allure.step("Убрать паспорт заявителя из payload"):
            valid_marriage_payload.personalNumberOfPassport = None

        with allure.step("Отправить запрос"):
            response = user_api.send_user_request(valid_marriage_payload)
            logger.info(f"Response body: {response.text}")

        with allure.step("Проверить что статус код не 200"):
            assert response.status_code == 400, (
                f"Ожидался код ошибки, получен {response.status_code}"
            )

        with allure.step("Проверить структуру ответа ошибки через Pydantic модель"):
            error = UserBadRequest(**response.json())
            assert error.code is not None

    @allure.title("POST /sendUserRequest — пустое значение в поле места рождения → 400")
    @allure.story("Негативные сценарии")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_send_request_without_passport_returns_error(self, user_api, valid_birth_payload):
        with allure.step("Убрать значение поля места рождения из payload"):
            valid_birth_payload.birth_place = None

        with allure.step("Отправить запрос"):
            response = user_api.send_user_request(valid_birth_payload)
            logger.info(f"Response body: {response.text}")

        with allure.step("Проверить что статус код не 200"):
            assert response.status_code == 400, (
                f"Ожидался код ошибки, получен {response.status_code}"
            )

        with allure.step("Проверить структуру ответа ошибки через Pydantic модель"):
            error = UserBadRequest(**response.json())
            assert error.code is not None
