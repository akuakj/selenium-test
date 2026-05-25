import pytest
import allure
from allure_commons.types import Severity
from API.models.application_models import GetApplicationsResponse
from utils.logger import get_logger

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
            parser = GetApplicationsResponse(**response.json())

        with allure.step("Проверить что присутствуют атрибуты applicationid и kindofapplication"):
            assert hasattr(parser.data[0], "applicationid") and hasattr(parser.data[0], "kindofapplication")

    @allure.title("GET /getApplications - получить указанное количество заявок")
    @allure.story("Получение заданного кол-ва заявок")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.positive
    @pytest.mark.parametrize("page, given_quantity", [
        (1, 5),
        (1, 10),
        (2, 3),
    ])
    def test_get_applications_given_quantity(self, application_api, page, given_quantity):

        with allure.step(f"Установить параметры: page={page}, limit={given_quantity}"):
            params = {
                "page": page,
                "limit": given_quantity
            }
            logger.info(f"Параметры запуска {params}")

        with allure.step("Отправить запрос с параметрами"):
            url = application_api.client.url(f'/getApplications')
            response =application_api.client.session.get(url, params=params)
            logger.info(f"Фактический URL: {response.request.url}")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, f"ожидался 200, фактический {response.status_code}"
            logger.info(f"Response status code: {response.status_code}")

        with allure.step("сравнить ответ с пайдентик моделью"):
            parser = GetApplicationsResponse(**response.json())

        with allure.step("Проверить что присутствуют атрибуты applicationid и kindofapplication"):
            assert hasattr(parser.data[0], "applicationid") and hasattr(parser.data[0], "kindofapplication")

        with allure.step("Проверить что количество записей совпадает с заданным given_quantity"):
            assert given_quantity == len(parser.data), f"Заданное количество записей {given_quantity} не совпадает с фактическим количеством {len(parser.data)}"


