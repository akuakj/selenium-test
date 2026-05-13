from faker import Faker
fake = Faker('ru_RU')
from pages.service_page import ServicePage
from pages.citizen_page import CitizenPage
from pages.enums import Gender

def _fill_citizen_general(driver, service: str):
    if service == 'marriage':
        ServicePage(driver).select_marriage()
    elif service == 'birth':
        ServicePage(driver).select_birth()
    citizen_page = CitizenPage(driver)
    citizen_page.fill_citizen_page(
        surname=fake.last_name(),
        name=fake.first_name(),
        midname=fake.middle_name(),
        birthdate=fake.date_of_birth(minimum_age=16).strftime('%d.%m.%Y'),
        passport=fake.bothify('??######', letters='АВРОНТСК'),
        gender=fake.random_element([g.value for g in Gender]),
        address=fake.address()
    )
    citizen_page.click_next()
