from playwright.sync_api import Page


class CitizenPage:
    CITIZEN_SURNAME = "input[maxlength='100']"
    CITIZEN_NAME = "input[maxlength='100']"
    CITIZEN_MIDNAME = "input[maxlength='100']"
    CITIZEN_DATE_OF_BIRTH = "input[type='date']"
    CITIZEN_PASSPORT = "input[maxlength='8']"
    CITIZEN_GENDER = "input[maxlength='4']"
    CITIZEN_ADDRESS = "input[placeholder='Введите адрес прописки']"

    BTN_NEXT = "button:has-text('Далее')"
    BTN_BACK = "button:has-text('Назад')"
    BTN_CLOSE = "button:has-text('Закрыть')"

    def __init__(self, page: Page):
        self.page = page

    def fill_citizen(self, surname: str, name: str, midname: str, birth: str, passport: str, gender: str, address: str):
        self.page.locator(self.CITIZEN_SURNAME).nth(0).fill(surname)
        self.page.locator(self.CITIZEN_NAME).nth(1).fill(name)
        self.page.locator(self.CITIZEN_MIDNAME).nth(2).fill(midname)
        self.page.locator(self.CITIZEN_DATE_OF_BIRTH).fill(birth)
        self.page.locator(self.CITIZEN_PASSPORT).fill(passport)
        self.page.locator(self.CITIZEN_GENDER).fill(gender)
        self.page.locator(self.CITIZEN_ADDRESS).fill(address)

    def click_next(self):
        self.page.locator(self.BTN_NEXT).click()

    def click_back(self):
        self.page.locator(self.BTN_BACK).click()

    def click_close(self):
        self.page.locator(self.BTN_CLOSE).click()