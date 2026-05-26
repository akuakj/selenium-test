import pytest
from faker import Faker
from API.client import ApiClient
from API.endpoints.user_api import UserAPI
from API.endpoints.appilication_api import ApplicationAPI
from API.endpoints.admin_api import AdminAPI
from API.models.user_models import UserRequest
from database.queries import db_queries

fake = Faker('ru_RU')


@pytest.fixture(scope="session")
def api_client():
    return ApiClient()


@pytest.fixture(scope="session")
def user_api(api_client):
    return UserAPI(api_client)


@pytest.fixture(scope="session")
def application_api(api_client):
    return ApplicationAPI(api_client)


@pytest.fixture(scope="session")
def admin_api(api_client):
    return AdminAPI(api_client)

@pytest.fixture(scope="session")
def created_application_id(user_api):
    payload = UserRequest(
        mode="wedding",
        personalLastName="Тестов",
        personalFirstName="Тест",
        personalMiddleName="Тестович",
        personalPhoneNumber="12345678901",
        personalNumberOfPassport="АВ123456",
        personalAddress="г. Москва, ул. Тестовая, д. 1",
        citizenLastName="Гражданов",
        citizenFirstName="Гражданин",
        citizenMiddleName="Гражданович",
        citizenBirthDate="01.01.1990",
        citizenNumberOfPassport="РО654321",
        citizenGender="муж",
        citizenAddress="г. Москва, ул. Гражданская, д. 2",
        dateOfMarriage="01.06.2025",
        newLastName="Тестов",
        anotherPersonLastName="Супругова",
        anotherPersonFirstName="Супруга",
        anotherPersonMiddleName="Супруговна",
        birth_of_anotoherPerson="01.01.1992",
        anotherPersonPassport="СК789012",
    )
    response = user_api.send_user_request(payload)
    return response.json()["data"]["applicationid"]

@pytest.fixture(scope="session")
def db():
    return db_queries
