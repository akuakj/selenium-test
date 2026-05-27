from datetime import date

import pytest
import allure
from allure_commons.types import Severity
from api.models.application_models import ResponseNotFound, GetApplStatusResponse
from utils.logger import get_logger

logger = get_logger(__name__)

@allure.epic('api')
@allure.feature('Тестирование get-запросов')
class TestGetApplStatus:

    @allure.title("GET /getApplStatus/{id} - получить заявку по существующему ID")
    @allure.story("Получение заявки по id")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_get_application_by_id_returns_200(self, application_api, created_application_id, db_client):
        with allure.step(f"отправить запрос на получение заявки с ID {created_application_id}"):
            response = application_api.get_application_by_id(created_application_id)
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.json()}")

        with allure.step("проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("проверить структуру ответа"):
            status_body_response = GetApplStatusResponse(**response.json())

        with allure.step("получить данные заявки из БД"):
            db_application = db_client.get_application_by_id(created_application_id)
            logger.info(f"DB application: id={db_application.applicationid}, kind={db_application.kindofapplication}, status={db_application.statusofapplication}")


        with allure.step("проверить что данные ответа соответствуют данным в БД"):
            assert status_body_response.data.kindofapplication == db_application.kindofapplication
            assert status_body_response.data.statusofapplication == db_application.statusofapplication

    @allure.title("GET /getApplStatus/{id} - несуществующий ID возвращает 404")
    @allure.story("Получение заявки по id")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_get_application_by_invalid_id_returns_404(self, application_api):
        invalid_id = -1

        with allure.step(f"отправить запрос с несуществующим ID {invalid_id}"):
            response = application_api.get_application_by_id(invalid_id)
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")

        with allure.step("Проверить структуру ошибки через Pydantic модель"):
            status_body_response = ResponseNotFound(**response.json())
            logger.info(f"Parsed error: code={status_body_response.code}, message={status_body_response.message}")

        with allure.step("проверить статус код 404"):
            assert status_body_response.code == 404
