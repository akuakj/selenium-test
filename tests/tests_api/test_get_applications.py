import pytest
import allure
from allure_commons.types import Severity
from API.models.application_models import GetApplicationsResponse
from logger import get_logger

logger = get_logger(__name__)

@allure.epic('API')
@allure.feature('Тестирование get-запросов')
class TestGetApplications:

    @allure.title("GET /getApplications - получить список всех заявок")
    @allure.story("Получение всех заявок услуг")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_get_all_applications(self, application_api):

        with allure.step("Отправить запрос на получние всех заявок"):
            response = application_api.get_all_applications()
            logger.info(f"Response status: {response.status_code}")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, f"Ожидался 200, фактический {response.status_code}"

        with allure.step("Проверить структуру ответа с пайдентик моделью"):
            parsed = GetApplicationsResponse(**response.json())

        with allure.step("Проверить что значение total равен с длиной списка data"):
            assert hasattr(parsed.data[0], "applicationid") and hasattr(parsed.data[0], "kindofapplication")