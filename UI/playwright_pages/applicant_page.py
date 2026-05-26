from playwright.sync_api import Page


class ApplicantPage:
    APPLICANT_SURNAME = "input[placeholder*='Введите фамилию']"
    APPLICANT_NAME = "input[placeholder*='Введите имя']"
    APPLICANT_MIDNAME = "input[placeholder*='Введите отчество']"
    APPLICANT_PHONE = "input[placeholder*='Введите номер телефона']"
    APPLICANT_PASSPORT = "input[placeholder*='Введите номер паспорта']"
    APPLICANT_ADDRESS = "input[placeholder*='Введите адрес прописки']"

    BTN_NEXT = "button:has-text('Далее')"
    BTN_CLOSE = "button:has-text('Закрыть')"

    def __init__(self, page: Page):
        self.page = page

    def fill_applicant(self, surname: str, name: str, midname: str,
                       phone: str, passport: str, address: str):
        self.page.locator(self.APPLICANT_SURNAME).fill(surname)
        self.page.locator(self.APPLICANT_NAME).fill(name)
        self.page.locator(self.APPLICANT_MIDNAME).fill(midname)
        self.page.locator(self.APPLICANT_PHONE).fill(phone)
        self.page.locator(self.APPLICANT_PASSPORT).fill(passport)
        self.page.locator(self.APPLICANT_ADDRESS).fill(address)

    def click_next(self):
        self.page.locator(self.BTN_NEXT).click()

    def click_close(self):
        self.page.locator(self.BTN_CLOSE).click()

