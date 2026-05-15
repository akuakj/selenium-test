import allure
import pytest
from logger import get_logger
from allure_commons.types import Severity
from API.models.admin_models import AdminResponse, ProcessResponse, AdminBadRequest
from API.data.admin_data import get_valid_admin_payload, get_process_request_payload
from API.data.user_data import get_valid_marriage_payload

logger = get_logger(__name__)

@allure.epic("API")
@allure.feature("Тестирование admin-запросов")
class TestAdminAPI:

    @allure.title("POST /sendAdminRequest - регистрация админа, валидные данные - 200")
    @allure.story("Регистрация админа")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_send_admin_request_returns_200(self, admin_api):

        with allure.step("Подготовить валидные данные для регистрации админа"):
            admin_payload = get_valid_admin_payload()
            logger.info(f"Payload: {admin_payload.model_dump()}")

        with allure.step("отправить валидный запрос на регистрацию админа"):
            response = admin_api.send_admin_request(admin_payload)
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
            assert parsed.data.staffid > 0,  f"staffid должен быть > 0, получен {parsed.data.staffid}"


    @allure.title("POST /sendAdminRequest — пустое поле фамилии → 400")
    @allure.story("Регистрация админа")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.negative
    def test_send_admin_request_without_surname_returns_error(self, admin_api):

        with allure.step("Подготовить данные с пустой фамилией"):
            admin_payload = get_valid_admin_payload(personalLastName=None)

        with allure.step("Отправить запрос"):
            response = admin_api.send_admin_request(admin_payload)
            logger.info(f"Response body: {response.text}")

        with allure.step("Проверить структуру ответа ошибки через Pydantic модель"):
            error = AdminBadRequest(**response.json())
            assert hasattr(error, "code") and hasattr(error, "message")


    @allure.title("POST /requestProcess - админ одобряет заявку")
    @allure.story("Проверка заявок")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_admin_approves_application(self, admin_api, user_api):

        with allure.step("Создать заявку на регистрацию брака"):
            marriage_payload = get_valid_marriage_payload()
            user_response = user_api.send_user_request(marriage_payload)
            logger.info(f"User response status: {user_response.status_code}")
            assert user_response.status_code == 200, "Не удалось создать заявку"
            applicationid = user_response.json()["data"]["applicationid"]
            logger.info(f"Создана заявка с applicationid: {applicationid}")

        with allure.step("Создать payload для регистрации админа"):
            admin_payload = get_valid_admin_payload()
            logger.info(f"Admin payload: {admin_payload.model_dump()}")

        with allure.step("POST /sendAdminRequest - Отправить запрос на регистрацию"):
            admin_registration_response = admin_api.send_admin_request(admin_payload)
            logger.info(f"Response status: {admin_registration_response.status_code}")
            logger.info(f"Response body: {admin_registration_response.json()}")

        with allure.step("Проверить, что регистрация успешно"):
            assert admin_registration_response.status_code == 200, (
                f"Ожидался 200, получен {admin_registration_response.status_code}: {admin_registration_response.text}"
            )

        with allure.step("Получить staffid"):
            staffid = admin_registration_response.json()["data"]["staffid"]
            logger.info(f"Получен staffid {staffid}")
            assert staffid > 0, f"staffid должен быть > 0, получен {staffid}"

        with allure.step("Создать payload для проверки заявки"):
            process_payload = get_process_request_payload(
                applicationid=applicationid,
                staffid=staffid,
                action="approved"
            )
            logger.info(f"Process payload: {process_payload.model_dump()}")

        with allure.step("POST /requestProcess - Отправить запрос на проверку заявки"):
            process_response = admin_api.request_process(process_payload)
            logger.info(f"Response status: {process_response.status_code}")
            logger.info(f"Response body: {process_response.json()}")

        with allure.step("Проверить, что заявка проверена успешно"):
            assert process_response.status_code == 200, (
                f"Ожидался 200, получен {process_response.status_code}"
            )

        with allure.step("Проверить структуру ответа через Pydantic"):
            parsed = ProcessResponse(**process_response.json())

        with allure.step("Проверить статус заявки (должен быть одобрен)"):
            assert parsed.data.statusofapplication == "approved", (
                f"Ожидался статус 'approved', получен {parsed.data.statusofapplication}"
            )

        with allure.step("Проверить что applicationid совпадает"):
            assert parsed.data.applicationid == applicationid


