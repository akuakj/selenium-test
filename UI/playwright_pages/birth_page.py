from playwright.sync_api import Page


class BirthPage:
    PLACE_OF_BIRTH = "input[maxlength='50']"
    MOTHER = "input[maxlength='20']"
    FATHER = "input[maxlength='20']"
    GRANNY = "input[maxlength='20']"
    GRANDDAD = "input[maxlength='20']"

    BTN_FINISH = "button:has-text('Завершить')"
    BTN_BACK = "button:has-text('Назад')"
    BTN_CLOSE = "button:has-text('Закрыть')"

    def __init__(self, page: Page):
        self.page = page

    def fill_birth(self, place: str, mother: str, father: str, granny: str, granddad: str):
        self.page.locator(self.PLACE_OF_BIRTH).fill(place)
        self.page.locator(self.MOTHER).nth(0).fill(mother)
        self.page.locator(self.FATHER).nth(1).fill(father)
        self.page.locator(self.GRANNY).nth(2).fill(granny)
        self.page.locator(self.GRANDDAD).nth(3).fill(granddad)

    def click_finish(self):
        self.page.locator(self.BTN_FINISH).click()

    def click_back(self):
        self.page.locator(self.BTN_BACK).click()

    def click_close(self):
        self.page.locator(self.BTN_CLOSE).click()