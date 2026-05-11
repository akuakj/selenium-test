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

