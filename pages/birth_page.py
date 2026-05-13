from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.status_page import StatusPage

class BirthLocators:
    PLACE_OF_BIRTH = (By.XPATH, "(//input[@maxlength='50'])")
    MOTHER = (By.XPATH, "(//input[@maxlength='20'])[1]")
    FATHER = (By.XPATH, "(//input[@maxlength='20'])[2]")
    GRANNY = (By.XPATH, "(//input[@maxlength='20'])[3]")
    GRANDDAD = (By.XPATH, "(//input[@maxlength='20'])[4]")
    FINISH_BUTTON = (By.XPATH, "//button[contains(text(), 'Завершить')]")


class BirthPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def fill_place_of_birth(self, place_of_birth):
        field = self.wait.until(EC.presence_of_element_located(BirthLocators.PLACE_OF_BIRTH))
        field.clear()
        field.send_keys(place_of_birth)
        return self

    def fill_mother(self, mother):
        field = self.wait.until(EC.presence_of_element_located(BirthLocators.MOTHER))
        field.clear()
        field.send_keys(mother)
        return self

    def fill_father(self, father):
        field = self.wait.until(EC.presence_of_element_located(BirthLocators.FATHER))
        field.clear()
        field.send_keys(father)
        return self

    def fill_granny(self, granny):
        field = self.wait.until(EC.presence_of_element_located(BirthLocators.GRANNY))
        field.clear()
        field.send_keys(granny)
        return self

    def fill_granddad(self, granddad):
        field = self.wait.until(EC.presence_of_element_located(BirthLocators.GRANDDAD))
        field.clear()
        field.send_keys(granddad)
        return self

    def fill_birth_page(self, place_of_birth, mother, father, granny, grandad):
        self.fill_place_of_birth(place_of_birth)
        self.fill_mother(mother)
        self.fill_father(father)
        self.fill_granny(granny)
        self.fill_granddad(grandad)
        return self

    def click_finish(self):
        button = self.wait.until(EC.element_to_be_clickable(BirthLocators.FINISH_BUTTON))
        button.click()
        return StatusPage(self.driver)

    def check_finish_button_disabled(self):
        button = self.wait.until(EC.presence_of_element_located(BirthLocators.FINISH_BUTTON))
        disabled = button.get_attribute("disabled")
        assert disabled is not None and disabled != 'false', "Кнопка Далее должна быть неактивной"

    def check_finish_button_enabled(self):
        button = self.wait.until(EC.presence_of_element_located(BirthLocators.FINISH_BUTTON))
        disabled = button.get_attribute("disabled")
        assert disabled is None or disabled == 'false', "Кнопка Далее должна быть активной"
