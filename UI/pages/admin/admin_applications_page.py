import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from UI.pages.admin.applications_table import ApplicationsTable


class AdminApplicationsLocators:
    UPDATE_BUTTON = (By.XPATH, "//button[contains(text(),'Обновить')]")
    CLOSE_BUTTON = (By.XPATH, "//button[contains(text(),'Закрыть')]")


class AdminApplicationsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.table = ApplicationsTable(driver)  # ← Page Element

    @allure.step("Нажать Обновить")
    def click_refresh(self):
        button = self.wait.until(EC.element_to_be_clickable(AdminApplicationsLocators.UPDATE_BUTTON))
        button.click()

    @allure.step("Нажать Закрыть")
    def click_close(self):
        button = self.wait.until(EC.element_to_be_clickable(AdminApplicationsLocators.CLOSE_BUTTON))
        button.click()