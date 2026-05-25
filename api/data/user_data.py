from faker import Faker
from API.models.user_models import UserRequest
from utils.fill_citizen_page import Gender

fake = Faker('ru_RU')


def get_valid_marriage_payload(**kwargs):
    valid_value = {
        "mode": "wedding",
        "personalLastName": fake.last_name(),
        "personalFirstName": fake.first_name(),
        "personalMiddleName": fake.middle_name(),
        "personalPhoneNumber": fake.numerify('########'),
        "personalNumberOfPassport": fake.bothify('??#####', letters='АВРОНСТ'),
        "personalAddress": fake.street_address(),
        "citizenLastName": fake.last_name(),
        "citizenFirstName": fake.first_name(),
        "citizenMiddleName": fake.middle_name(),
        "citizenBirthDate": fake.date_of_birth(minimum_age=16).strftime('%Y-%m-%d'),
        "citizenNumberOfPassport": fake.bothify('??#####', letters='АВРОНСТ'),
        "citizenGender": fake.random_element([g.value for g in Gender]),
        "citizenAddress": fake.street_address(),
        "dateOfMarriage": fake.date_between().strftime('%Y-%m-%d'),
        "newLastName": fake.last_name(),
        "anotherPersonLastName": fake.last_name(),
        "anotherPersonFirstName": fake.first_name(),
        "anotherPersonMiddleName": fake.middle_name(),
        "birth_of_anotoherPerson": fake.date_of_birth(minimum_age=16).strftime('%Y-%m-%d'),
        "anotherPersonPassport": fake.bothify('??#####', letters='АВРОНСТ'),
    }
    valid_value.update(kwargs)
    return UserRequest(**valid_value)


def get_valid_birth_payload(**kwargs):
    valid_value = {
        "mode": "birth",
        "personalLastName": fake.last_name(),
        "personalFirstName": fake.first_name(),
        "personalMiddleName": fake.middle_name(),
        "personalPhoneNumber": fake.numerify('########'),
        "personalNumberOfPassport": fake.bothify('??#####', letters='АВРОНСТ'),
        "personalAddress": fake.street_address(),
        "citizenLastName": fake.last_name(),
        "citizenFirstName": fake.first_name(),
        "citizenMiddleName": fake.middle_name(),
        "citizenBirthDate": fake.date_of_birth(minimum_age=16).strftime('%Y-%m-%d'),
        "citizenNumberOfPassport": fake.bothify('??#####', letters='АВРОНСТ'),
        "citizenGender": fake.random_element([g.value for g in Gender]),
        "citizenAddress": fake.street_address(),
        "birth_place": fake.street_address(),
        "birth_mother": fake.first_name(),
        "birth_father": fake.first_name(),
        "birth_grandma": fake.first_name(),
        "birth_grandpa": fake.first_name()
    }
    valid_value.update(kwargs)
    return UserRequest(**valid_value)