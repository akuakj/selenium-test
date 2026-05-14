import allure
import pytest
from faker import Faker
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from UI.pages.citizen_page import CitizenLocators
from allure_commons.types import Severity

fake = Faker('ru_RU')

@allure.feature("Данные услуг")
class TestServicePage:

    @allure.title("Выбрать услугу регистрации брака")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_marriage_service_opens_citizen_page(self, driver, service_page_ready):
        service_page_ready.select_marriage()
        field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(CitizenLocators.CITIZEN_SURNAME)
        )
        assert field is not None

    @allure.title("Выбрать услугу регистрации рождения")
    @allure.story("Позитивные сценарии")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.positive
    def test_birth_service_opens_citizen_page(self, driver, service_page_ready):
        service_page_ready.select_birth()
        field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(CitizenLocators.CITIZEN_SURNAME)
        )
        assert field is not None

