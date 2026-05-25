import pytest
import allure
from allure_commons.types import Severity
from API.models.application_models import ResponseNotFound, GetApplStatusResponse
from utils.logger import get_logger

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
# проверить не через none
        with allure.step("Проверить что статус заявки не пустой"):
            assert parsed.data.statusofapplication, "Поле statusofapplication пустое"

        with allure.step("Проверить что тип заявки не пустой"):
            assert parsed.data.kindofapplication, "Поле kindofapplication пустое"

        with allure.step("проверить что тип заявки соответствует ожидаемому"):
            assert parsed.data.kindofapplication in ["Получение свидетельства о браке", "Получение свидетельства о рождении", "Получение свидетельства о смерти"]

    @allure.title("GET /getApplStatus/{id} - несуществующий ID возвращает 404")
    @allure.story("Получение заявки по id")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_get_application_by_invalid_id_returns_404(self, application_api):
        invalid_id = -1

        with allure.step(f"отправить запрос с несуществующим ID {invalid_id}"):
            response = application_api.get_application_by_id(invalid_id)

        with allure.step("Проверить статус код 404"):
            assert response.status_code == 404, (
                f"Ожидался 404, получен {response.status_code}"
            )

        with allure.step("Проверить структуру ошибки через Pydantic модель"):
            parsed = ResponseNotFound(**response.json())

        with allure.step("Проверить что сообщение об ошибке не пустое"):
            assert parsed.message, "Поле message в ответе ошибки пустое"

        with allure.step("проверить статус код 404"):
            assert parsed.code == 404
