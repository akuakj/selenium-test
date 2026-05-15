from faker import Faker
from API.models.admin_models import AdminRequest, ProcessRequest

fake = Faker('ru_RU')

def get_valid_admin_payload(**overrides):
    valid_value = {
        "personalLastName": fake.last_name(),
        "personalFirstName": fake.first_name(),
        "personalMiddleName": fake.middle_name(),
        "personalPhoneNumber": fake.numerify("########"),
        "personalNumberOfPassport": fake.bothify('??#####', letters='АВРОНСТ'),
        "dateofbirth": fake.date_of_birth(minimum_age=18).strftime('%Y-%m-%d')
    }
    valid_value.update(overrides)
    return AdminRequest(**valid_value)


def get_process_request_payload(applicationid: int, staffid: int, action: str = "approve"):
    return ProcessRequest(
        applId=applicationid,
        staffid=staffid,
        action=action
    )