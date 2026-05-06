from selenium.webdriver.common.by import By
from base_page import BasePage

class BirthForm(BasePage):

    PLACE_OF_BIRTH = (By.XPATH, "(//input[@maxlength='50'])")
    MOTHER = (By.XPATH, "(//input[@maxlength='20'])[1]")
    FATHER = (By.XPATH, "(//input[@maxlength='20'])[2]")
    GRANNY = (By.XPATH, "(//input[@maxlength='20'])[3]")
    GRANDDAD = (By.XPATH, "(//input[@maxlength='20'])[4]")
    FINISH_BUTTON = (By.XPATH, "//button[contains(text(), 'Завершить')]")

    def __init__(self, driver):
        super().__init__(driver)

    def fill_place_of_birth(self, place_of_birth):
        self.input_text(self.PLACE_OF_BIRTH, place_of_birth)

    def fill_mother(self, mother):
        self.input_text(self.MOTHER, mother)

    def fill_father(self, father):
        self.input_text(self.FATHER, father)

    def fill_granny(self, granny):
        self.input_text(self.GRANNY, granny)

    def fill_granddad(self, granddad):
        self.input_text(self.GRANDDAD, granddad)

    def click_finish(self):
        self.click(self.FINISH_BUTTON)
        print("Шаг 4 → нажата кнопка 'Завершить'")