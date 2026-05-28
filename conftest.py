import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from faker import Faker
from UI.pages.home_page import HomePage
from UI.pages.applicant_page import ApplicantPage
from UI.pages.service_page import ServicePage
from UI.pages.citizen_page import CitizenPage
from UI.pages.marriage_page import MarriagePage
from UI.pages.birth_page import BirthPage
from UI.pages.admin_registration_page import AdminRegistrationPage
from UI.pages.admin_applications_page import AdminApplicationsPage
from utils.fill_citizen_page import fill_citizen_general


USE_SELENOID = os.getenv("USE_SELENOID", "false").lower() == "true"
SELENOID_URL = os.getenv("SELENOID_URL", "http://localhost:4444/wd/hub")

fake = Faker('ru-RU')

@pytest.fixture(scope="function")
def driver():

    if USE_SELENOID:
        driver = _build_selenoid_driver()
    else:
        driver = _build_local_driver()

    driver.maximize_window()
    yield driver
    driver.quit()


def _build_local_driver() -> WebDriver:
    options = Options()
    return webdriver.Chrome(options=options)


def _build_selenoid_driver() -> WebDriver:
    options = Options()
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", "128.0")
    options.set_capability(
        "selenoid:options",
        {
            # Включить запись видео для упавших тестов
            "enableVideo": False,
            # Включить VNC (нужно для selenoid-ui live-view)
            "enableVNC": True,
            # Логи браузера
            "enableLog": True,
            # Имя теста появится в selenoid-ui
            "name": "zagss-ui-tests",
        },
    )
    return webdriver.Remote(
        command_executor=SELENOID_URL,
        options=options,
    )

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
    fill_citizen_general(driver, 'marriage')

@pytest.fixture
def citizen_done_for_birth(driver, applicant_done):
    fill_citizen_general(driver, 'birth')

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



