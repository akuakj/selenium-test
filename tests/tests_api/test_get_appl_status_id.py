import pytest
import allure
from allure_commons.types import Severity
from API.models.application_models import ResponseNotFound, GetApplStatusResponse
from API.data.user_data import get_valid_marriage_payload
from logger import get_logger

logger = get_logger(__name__)

@allure.epic('API')
@allure.feature('Тестирование get-запросов')
class TestGetApplStatus:

    @allure.title("GET /getApplStatus/{id} - получить заявку по существующему ID")
    @allure.story("Получение заявки по id")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_get_application_by_id_returns_200(self, application_api, created_application_id):
        with allure.step(f"отправить запрос на получение заявки с ID {created_application_id}"):
            response = application_api.get_application_by_id(created_application_id)
            logger.info(f"Response status: {response.status_code}")

        with allure.step("проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("проверить структуру ответа"):
            parsed = GetApplStatusResponse(**response.json())

        with allure.step("проверить что статус заявки не пустой"):
            assert parsed.data.statusofapplication is not None
            assert parsed.data.kindofapplication is not None

        with allure.step("проверить что тип заявки соответствует ожидаемому"):
            assert parsed.data.kindofapplication in ["Получение свидетельства о браке", "Получение свидетельства о рождении", "Получение свидетельства о смерти"]

    @allure.title("GET /getApplStatus/{id} - несуществующий ID возвращает 404")
    @allure.story("Негативные сценарии")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_get_application_by_invalid_id_returns_404(self, application_api):
        invalid_id = -1

        with allure.step(f"отправить запрос с несуществующим ID {invalid_id}"):
            response = application_api.get_application_by_id(invalid_id)

        with allure.step("проверить структуру ошибки"):
            parsed = ResponseNotFound(**response.json())
            assert parsed.code is not None
            assert parsed.message is not None

        with allure.step("проверить статус код 404"):
            assert parsed.code == 404
