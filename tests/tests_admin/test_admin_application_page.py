import pytest
from faker import Faker
from pages.enums import ApplicationStatus
import allure
from allure_commons.types import Severity

fake = Faker('ru_RU')

@allure.feature("Администрация заявок")
class TestAdminApplicationsPage:

    @allure.title("Одобрение первой заявки в таблице")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_approve_changes_status(self, driver, admin_applications_ready):
        first_row = admin_applications_ready.table.get_first_row()
        app_number = admin_applications_ready.table.get_number(first_row)
        admin_applications_ready.table.approve_first()
        row = admin_applications_ready.table.get_row_by_number(app_number)
        assert admin_applications_ready.table.get_status(row) == ApplicationStatus.APPROVED.value

    @allure.title("Отклонение первой заявки в таблице")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_reject_changes_status(self, driver, admin_applications_ready):
        first_row = admin_applications_ready.table.get_first_row()
        app_number = admin_applications_ready.table.get_number(first_row)
        admin_applications_ready.table.reject_first()
        row = admin_applications_ready.table.get_row_by_number(app_number)
        assert admin_applications_ready.table.get_status(row) == ApplicationStatus.REJECTED.value

    @allure.title("В таблице есть строки с заявками")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_table_has_rows(self, driver, admin_applications_ready):
        rows = admin_applications_ready.table.get_rows()
        assert len(rows) > 0
