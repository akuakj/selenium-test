from playwright.sync_api import Page


class ServicePage:
    BTN_MARRIAGE = 'text=Регистрация брака'
    BTN_BIRTH = 'text=Регистрация рождения'
    BTN_DEATH = 'text=Регистрация смерти'

    BTN_BACK = 'text=Назад'
    BTN_CLOSE = 'text=Закрыть'

    def __init__(self, page: Page):
        self.page = page

    def select_marriage(self):
        self.page.locator(self.BTN_MARRIAGE).click()

    def select_birth(self):
        self.page.locator(self.BTN_BIRTH).click()

    def select_death(self):
        self.page.locator(self.BTN_DEATH).click()

    def click_back(self):
        self.page.locator(self.BTN_BACK).click()

    def click_close(self):
        self.page.locator(self.BTN_CLOSE).click()