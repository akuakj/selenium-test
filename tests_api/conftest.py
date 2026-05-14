import pytest
from faker import Faker
from api.client import ApiClient
from api.endpoints.user_api import UserAPI
from api.endpoints.appilication_api import ApplicationAPI
from api.endpoints.admin_api import AdminAPI
from api.models.user_models import UserRequest
from api.models.admin_models import AdminRequest
from pages.enums import Gender
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

@pytest.fixture
def valid_marriage_payload():
    return UserRequest(
        mode="wedding",
        personalLastName= fake.last_name(),
        personalFirstName=fake.first_name(),
        personalMiddleName=fake.middle_name(),
        personalPhoneNumber=fake.numerify('########'),
        personalNumberOfPassport=fake.bothify('??#####', letters='АВРОНСТ'),
        personalAddress=fake.street_address(),
        citizenLastName=fake.last_name(),
        citizenFirstName=fake.first_name(),
        citizenMiddleName=fake.middle_name(),
        citizenBirthDate=fake.date_of_birth(minimum_age=16).strftime('%Y-%m-%d'),
        citizenNumberOfPassport=fake.bothify('??#####', letters='АВРОНСТ'),
        citizenGender=fake.random_element([g.value for g in Gender]),
        citizenAddress=fake.street_address(),
        dateOfMarriage=fake.date_between().strftime('%Y-%m-%d'),
        newLastName=fake.last_name(),
        anotherPersonLastName=fake.last_name(),
        anotherPersonFirstName=fake.first_name(),
        anotherPersonMiddleName=fake.middle_name(),
        birth_of_anotoherPerson=fake.date_of_birth(minimum_age=16).strftime('%Y-%m-%d'),
        anotherPersonPassport=fake.bothify('??#####', letters='АВРОНСТ'),
    )

@pytest.fixture
def valid_birth_payload():
    return UserRequest(
        mode="birth",
        personalLastName= fake.last_name(),
        personalFirstName=fake.first_name(),
        personalMiddleName=fake.middle_name(),
        personalPhoneNumber=fake.numerify('########'),
        personalNumberOfPassport=fake.bothify('??#####', letters='АВРОНСТ'),
        personalAddress=fake.street_address(),
        citizenLastName=fake.last_name(),
        citizenFirstName=fake.first_name(),
        citizenMiddleName=fake.middle_name(),
        citizenBirthDate=fake.date_of_birth(minimum_age=16).strftime('%Y-%m-%d'),
        citizenNumberOfPassport=fake.bothify('??#####', letters='АВРОНСТ'),
        citizenGender=fake.random_element([g.value for g in Gender]),
        citizenAddress=fake.street_address(),
        birth_place=fake.street_address(),
        birth_mother=fake.name(),
        birth_father=fake.first_name(),
        birth_grandma=fake.first_name(),
        birth_grandpa=fake.first_name()
    )


@pytest.fixture
def valid_admin_payload():
    return AdminRequest(
        personalLastName="dfdsfsdf",
        personalFirstName="dfdsfsdf",
        personalMiddleName="dfdsfsdf",
        personalPhoneNumber='2132132',
        personalNumberOfPassport='А2312545',
        dateofbirth='1999.01.01'
    )


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

for i in range(100):
    print(len(fake.name()))