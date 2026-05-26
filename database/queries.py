from sqlalchemy import select
from database.client import DBClient
from database.models import ApplicantsModel, ApplicationsModel, StaffModel, CitizensModel, BirthCertificatesModel
from utils.logger import get_logger
from database.client import client as cl

logger = get_logger(__name__)


class DBQueries:
    def __init__(self, client: DBClient):
        self.client = client

    def get_applicant_by_id(self, applicant_id: int) -> ApplicantsModel | None:
        with self.client.session_scope() as session:
            stmt = select(ApplicantsModel).where(ApplicantsModel.applicantid == applicant_id)
            return session.execute(stmt).scalar_one_or_none()

    def get_applicant_by_passport(self, passport: str) -> ApplicantsModel | None:
        with self.client.session_scope() as session:
            stmt = select(ApplicantsModel).where(ApplicantsModel.passportnumber == passport)
            return session.execute(stmt).scalar_one_or_none()

    def get_staff_by_id(self, staff_id: int) -> StaffModel | None:
        with self.client.session_scope() as session:
            stmt = select(StaffModel).where(StaffModel.staffid == staff_id)
            return session.execute(stmt).scalar_one_or_none()

    def get_staff_by_passport(self, passport: str) -> StaffModel | None:
        with self.client.session_scope() as session:
            stmt = select(StaffModel).where(StaffModel.passportnumber == passport)
            return session.execute(stmt).scalar_one_or_none()

    def get_application_by_id(self, application_id: int) -> ApplicationsModel | None:
        with self.client.session_scope() as session:
            stmt = select(ApplicationsModel).where(ApplicationsModel.applicationid == application_id)
            return session.execute(stmt).scalar_one_or_none()

    def get_application_status(self, application_id: int) -> str | None:
        with self.client.session_scope() as session:
            stmt = select(ApplicationsModel.statusofapplication).where(
                ApplicationsModel.applicationid == application_id
            )
            return session.execute(stmt).scalar_one_or_none()

    def get_citizen_by_id(self, citizen_id: int) -> CitizensModel | None:
        with self.client.session_scope() as session:
            stmt = select(CitizensModel).where(CitizensModel.citizenid == citizen_id)
            return session.execute(stmt).scalar_one_or_none()

    def get_birth_certificate_by_citizen_id(self, citizen_id: int) -> BirthCertificatesModel | None:
        with self.client.session_scope() as session:
            stmt = select(BirthCertificatesModel).where(BirthCertificatesModel.citizenid == citizen_id)
            return session.execute(stmt).scalar_one_or_none()


db_queries = DBQueries(cl)