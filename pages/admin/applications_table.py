from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ApplicationsTableLocators:
    ROWS = (By.XPATH, "//tr[contains(@class, 'MuiTableRow-root') and not(ancestor::thead)]")
    APPROVE_BUTTON = (By.XPATH, ".//*[@data-testid='ThumbUpIcon']/ancestor::button")
    REJECT_BUTTON = (By.XPATH, ".//*[@data-testid='ThumbDownIcon']/ancestor::button")
    NUMBER_CELL = (By.XPATH, "./td[1]")
    APPLICANT_CELL = (By.XPATH, "./td[2]")
    TYPE_CELL = (By.XPATH, "./td[3]")
    TIME_CELL = (By.XPATH, "./td[4]")
    STATUS_CELL = (By.XPATH, "./td[5]")

class ApplicationsTable:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def get_rows(self):
        return self.wait.until(
            EC.presence_of_all_elements_located(ApplicationsTableLocators.ROWS)
        )

    def get_first_row(self):
        return self.get_rows()[0]

    def get_row_by_number(self, application_number: str):
        rows = self.get_rows()
        for row in rows:
            number = row.find_element(*ApplicationsTableLocators.NUMBER_CELL).text
            if number == application_number:
                return row
        return None

    def get_status(self, row):
        return row.find_element(*ApplicationsTableLocators.STATUS_CELL).text

    def get_number(self, row):
        return row.find_element(*ApplicationsTableLocators.NUMBER_CELL).text

    def approve(self, row):
        row.find_element(*ApplicationsTableLocators.APPROVE_BUTTON).click()

    def reject(self, row):
        row.find_element(*ApplicationsTableLocators.REJECT_BUTTON).click()

    def approve_first(self):
        self.approve(self.get_first_row())

    def reject_first(self):
        self.reject(self.get_first_row())

    def get_status_of_first_row(self):
        return self.get_status(self.get_first_row())