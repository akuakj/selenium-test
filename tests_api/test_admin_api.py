from api.models.admin_models import AdminResponse
from api.models.admin_models import AdminBadRequest
import allure
import pytest
from allure_commons.types import Severity
from logger import get_logger

logger = get_logger(__name__)


@allure.feature("Тестирование запросов администратора")
class TestAdminAPI:

    @allure.title("POST /sendAdminRequest - регистрация админа, валидные данные - 200")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_send_admin_request_returns_200(self, admin_api, valid_admin_payload):
        with allure.step("отправить валидный запрос на регистрацию админа"):
            response = admin_api.send_admin_request(valid_admin_payload)
            logger.info(f"Response body: {response.json()}")

        with allure.step("проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("проверить структуру ответа с пайдантик моделью"):
            parsed = AdminResponse(**response.json())

        with allure.step("в ответе присутсвует поле staffid"):
            assert hasattr(parsed.data, "staffid"), "Поле отсутствует в ответе"

        with allure.step("проверить что id больше 0"):
            assert parsed.data.staffid > 0

    @allure.title("POST /sendAdminRequest — пустоt поле фамилии → не 200")
    @allure.story("Негативные сценарии")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_send_admin_request_without_surname_returns_error(self, admin_api, valid_admin_payload):
        with allure.step("переопределить фамилию"):
            valid_admin_payload.personalLastName = ""

        with allure.step("Отправить запрос"):
            response = admin_api.send_admin_request(valid_admin_payload)
            logger.info(f"Response body: {response.text}")

        # with allure.step("Проверить что статус код не 200"):
        #     assert response.status_code != 200, (
        #         f"Ожидался код ошибки, получен {response.status_code}"
        #     )

        with allure.step("Проверить структуру ответа ошибки через Pydantic модель"):
            error = AdminBadRequest(**response.json())
            assert error.code == "error"