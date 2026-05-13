import pytest
from faker import Faker
from pages.enums import ApplicationStatus

fake = Faker('ru_RU')

class TestAdminApplicationsPage:

    @pytest.mark.positive
    def test_approve_changes_status(self, driver, admin_applications_ready):
        first_row = admin_applications_ready.table.get_first_row()
        app_number = admin_applications_ready.table.get_number(first_row)
        admin_applications_ready.table.approve_first()
        row = admin_applications_ready.table.get_row_by_number(app_number)
        assert admin_applications_ready.table.get_status(row) == ApplicationStatus.APPROVED.value

    @pytest.mark.positive
    def test_reject_changes_status(self, driver, admin_applications_ready):
        first_row = admin_applications_ready.table.get_first_row()
        app_number = admin_applications_ready.table.get_number(first_row)
        admin_applications_ready.table.reject_first()
        row = admin_applications_ready.table.get_row_by_number(app_number)
        assert admin_applications_ready.table.get_status(row) == ApplicationStatus.REJECTED.value

    @pytest.mark.positive
    def test_table_has_rows(self, driver, admin_applications_ready):
        rows = admin_applications_ready.table.get_rows()
        assert len(rows) > 0
