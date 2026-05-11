import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from faker import Faker
from pages.home_page import HomePage
from pages.applicant_page import ApplicantPage
from pages.service_page import ServicePage
from pages.citizen_page import CitizenPage
from pages.marriage_page import MarriagePage
from pages.birth_page import BirthPage

fake = Faker('ru_RU')

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def home_page(driver):
    home = HomePage(driver)
    home.open()
    return home

@pytest.fixture
def applicant_page_ready_user(driver, home_page):
    home_page.click_login_as_user()
    return ApplicantPage(driver)

@pytest.fixture
def applicant_done(driver, applicant_page_ready_user):
    applicant_page_ready_user.fill_applicant_page(
        surname=fake.last_name(),
        name=fake.first_name(),
        midname=fake.middle_name(),
        phone=fake.numerify('###########'),
        passport=fake.bothify('??######', letters='АВРСКЕОТН'),
        address=fake.address()
    )
    applicant_page_ready_user.click_next()

@pytest.fixture
def service_page_ready(driver, applicant_done):
    return ServicePage(driver)

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
        gender=fake.random_element(['муж', 'жен', 'м', 'ж']),
        address=fake.address()
    )
    citizen_page.click_next()

@pytest.fixture
def citizen_page_ready(driver, applicant_done):
    ServicePage(driver).select_marriage()
    return CitizenPage(driver)

@pytest.fixture
def citizen_done_for_marriage(driver, applicant_done):
    _fill_citizen_general(driver, 'marriage')

@pytest.fixture
def citizen_done_for_birth(driver, applicant_done):
    _fill_citizen_general(driver, 'birth')

@pytest.fixture
def marriage_page_ready(driver, citizen_done_for_marriage):
    return MarriagePage(driver)

@pytest.fixture
def birth_page_ready(driver, citizen_done_for_birth):
    return BirthPage(driver)



