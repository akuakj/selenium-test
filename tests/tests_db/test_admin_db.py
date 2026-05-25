import allure
import pytest
from allure_commons.types import Severity
from faker import Faker
from API.models.admin_models import AdminResponse
from API.data.user_data import get_valid_marriage_payload
from API.data.admin_data import get_valid_admin_payload, get_process_request_payload
from utils.enums import StatusOfApplicationAPI
from utils.logger import get_logger

fake = Faker('ru_RU')
logger = get_logger(__name__)


@allure.epic("API + DB")
@allure.feature("Проверка данных администраторов в БД")
class TestAdminDB:

    @allure.title("POST /sendAdminRequest — администратор сохраняется в БД")
    @allure.story("Создание админов")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_admin_saved_in_db(self, admin_api, db):

        with allure.step("Подготовить payload с фиксированным паспортом"):
            passport = fake.bothify('??#####', letters='АВРОНСТ')
            payload = get_valid_admin_payload(personalNumberOfPassport=passport)
            logger.info(f"Паспорт администратора: {passport}")

        with allure.step("POST /sendAdminRequest — зарегистрировать администратора"):
            response = admin_api.send_admin_request(payload)
            logger.info(f"Response {response.status_code}: {response.json()}")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}: {response.text}"
            )

        with allure.step("Получить staffid из ответа API"):
            parsed = AdminResponse(**response.json())
            staff_id = parsed.data.staffid
            logger.info(f"staffid: {staff_id}")
            assert staff_id > 0, f"staffid должен быть > 0, получен {staff_id}"

        with allure.step("Запросить администратора из БД по staffid"):
            staff = db.get_staff_by_id(staff_id)
            logger.info(f"Запись из БД: {staff}")

        with allure.step("Проверить что запись существует в БД"):
            assert staff, (
                f"Администратор с staffid={staff_id} не найден в БД"
            )

        with allure.step("Проверить что паспорт в БД совпадает с отправленным"):
            assert staff.passportnumber == passport, (
                f"Паспорт в БД: '{staff.passportnumber}', ожидался: '{passport}'"
            )

        with allure.step("Проверить что фамилия администратора не пустая"):
            assert staff.surname, "Поле surname в БД пустое"

        with allure.step("Проверить что имя администратора не пустое"):
            assert staff.name, "Поле name в БД пустое"

        with allure.step("Проверить что отчество администратора не пустое"):
            assert staff.middlename, "Поле middlename в БД пустое"

        with allure.step("Проверить что телефон администратора не пустой"):
            assert staff.phonenumber, "Поле phonenumber в БД пустое"

        with allure.step("Проверить что дата рождения администратора не пустая"):
            assert staff.dateofbirth, "Поле dateofbirth в БД пустое"

    @allure.title("POST /requestProcess (approve) — начальный статус заявки under consideration")
    @allure.story("Проверка заявок")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.positive
    def test_application_initial_status_is_under_consideration(self, user_api, db):

        with allure.step("Создать заявку на регистрацию брака"):
            user_response = user_api.send_user_request(get_valid_marriage_payload())
            assert user_response.status_code == 200, "Не удалось создать заявку"
            application_id = user_response.json()["data"]["applicationid"]
            logger.info(f"applicationid: {application_id}")

        with allure.step("Запросить статус заявки из БД сразу после создания"):
            status = db.get_application_status(application_id)
            logger.info(f"Начальный статус: {status}")

        with allure.step("Проверить что начальный статус — under consideration"):
            assert status == StatusOfApplicationAPI.UNDER_CONSIDERATION.value, (
                f"Ожидался '{StatusOfApplicationAPI.UNDER_CONSIDERATION.value}', получен '{status}'"
            )

    @allure.title("POST /requestProcess (approve) — статус заявки обновляется в БД")
    @allure.story("Проверка заявок")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_approve_application_updates_status_in_db(self, admin_api, user_api, db):

        with allure.step("Создать заявку на регистрацию брака"):
            user_response = user_api.send_user_request(get_valid_marriage_payload())
            assert user_response.status_code == 200, "Не удалось создать заявку"
            application_id = user_response.json()["data"]["applicationid"]
            logger.info(f"applicationid: {application_id}")

        with allure.step("Зарегистрировать администратора"):
            admin_response = admin_api.send_admin_request(get_valid_admin_payload())
            assert admin_response.status_code == 200, "Не удалось зарегистрировать администратора"
            staff_id = admin_response.json()["data"]["staffid"]
            logger.info(f"staffid: {staff_id}")

        with allure.step("Проверить начальный статус заявки в БД"):
            status_before = db.get_application_status(application_id)
            logger.info(f"Статус до approve: {status_before}")
            assert status_before == StatusOfApplicationAPI.UNDER_CONSIDERATION.value, (
                f"Ожидался '{StatusOfApplicationAPI.UNDER_CONSIDERATION.value}', получен '{status_before}'"
            )

        with allure.step("POST /requestProcess — одобрить заявку"):
            process_payload = get_process_request_payload(
                applicationid=application_id,
                staffid=staff_id,
                action=StatusOfApplicationAPI.APPROVED.value
            )
            process_response = admin_api.request_process(process_payload)
            assert process_response.status_code == 200, "Не удалось одобрить заявку"
            logger.info("Заявка одобрена через API")

        with allure.step("Проверить статус заявки в БД после approve"):
            status_after = db.get_application_status(application_id)
            logger.info(f"Статус после approve: {status_after}")
            assert status_after == StatusOfApplicationAPI.APPROVED.value, (
                f"Ожидался '{StatusOfApplicationAPI.APPROVED.value}', в БД: '{status_after}'"
            )

    @allure.title("POST /requestProcess (approve) — staffid привязывается к заявке в БД")
    @allure.story("Проверка заявок")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_approve_application_links_staff_in_db(self, admin_api, user_api, db):

        with allure.step("Создать заявку на регистрацию брака"):
            user_response = user_api.send_user_request(get_valid_marriage_payload())
            assert user_response.status_code == 200, "Не удалось создать заявку"
            application_id = user_response.json()["data"]["applicationid"]

        with allure.step("Зарегистрировать администратора"):
            admin_response = admin_api.send_admin_request(get_valid_admin_payload())
            assert admin_response.status_code == 200, "Не удалось зарегистрировать администратора"
            staff_id = admin_response.json()["data"]["staffid"]

        with allure.step("Проверить что staffid в заявке пустой до обработки"):
            application_before = db.get_application_by_id(application_id)
            assert application_before.staffid is None, (
                f"staffid должен быть None до обработки, получен {application_before.staffid}"
            )

        with allure.step("POST /requestProcess — одобрить заявку"):
            process_payload = get_process_request_payload(
                applicationid=application_id,
                staffid=staff_id,
                action=StatusOfApplicationAPI.APPROVED.value
            )
            process_response = admin_api.request_process(process_payload)
            assert process_response.status_code == 200, "Не удалось одобрить заявку"

        with allure.step("Проверить что staffid привязался к заявке в БД"):
            application_after = db.get_application_by_id(application_id)
            assert application_after.staffid == staff_id, (
                f"staffid в БД: {application_after.staffid}, ожидался: {staff_id}"
            )

    @allure.title("POST /requestProcess (reject) — статус заявки обновляется на rejected в БД")
    @allure.story("Проверка заявок")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.negative
    def test_reject_application_updates_status_in_db(self, admin_api, user_api, db):

        with allure.step("Создать заявку на регистрацию брака"):
            user_response = user_api.send_user_request(get_valid_marriage_payload())
            assert user_response.status_code == 200, "Не удалось создать заявку"
            application_id = user_response.json()["data"]["applicationid"]
            logger.info(f"applicationid: {application_id}")

        with allure.step("Зарегистрировать администратора"):
            admin_response = admin_api.send_admin_request(get_valid_admin_payload())
            assert admin_response.status_code == 200, "Не удалось зарегистрировать администратора"
            staff_id = admin_response.json()["data"]["staffid"]
            logger.info(f"staffid: {staff_id}")

        with allure.step("Проверить начальный статус заявки в БД"):
            status_before = db.get_application_status(application_id)
            assert status_before == StatusOfApplicationAPI.UNDER_CONSIDERATION.value, (
                f"Ожидался '{StatusOfApplicationAPI.UNDER_CONSIDERATION.value}', получен '{status_before}'"
            )

        with allure.step("POST /requestProcess — отклонить заявку"):
            process_payload = get_process_request_payload(
                applicationid=application_id,
                staffid=staff_id,
                action=StatusOfApplicationAPI.REJECTED.value
            )
            process_response = admin_api.request_process(process_payload)
            assert process_response.status_code == 200, "Не удалось отклонить заявку"
            logger.info("Заявка отклонена через API")

        with allure.step("Проверить статус заявки в БД после reject"):
            status_after = db.get_application_status(application_id)
            logger.info(f"Статус после reject: {status_after}")
            assert status_after == StatusOfApplicationAPI.REJECTED.value, (
                f"Ожидался '{StatusOfApplicationAPI.REJECTED.value}', в БД: '{status_after}'"
            )