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
from pages.admin.admin_registration_page import AdminRegistrationPage
from pages.admin.admin_applications_page import AdminApplicationsPage
from utils import _fill_citizen_general

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

@pytest.fixture
def admin_page_ready(driver, home_page):
    home_page.click_login_as_admin()
    return AdminRegistrationPage(driver)

@pytest.fixture
def admin_registration_done(driver, admin_page_ready):
    admin_page_ready.fill_admin_page(
        surname=fake.last_name(),
        name=fake.first_name(),
        midname=fake.middle_name(),
        phone=fake.numerify('#########'),
        passport=fake.bothify('??#######', letters='АВРСКЕОНТ'),
        birthdate = fake.date_of_birth(minimum_age=18).strftime('%d.%m.%Y')
    )
    admin_page_ready.click_next()

@pytest.fixture
def admin_applications_ready(driver, admin_registration_done):
    return AdminApplicationsPage(driver)