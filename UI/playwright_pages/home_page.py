from playwright.sync_api import Page


class HomePage:
    BTN_LOGIN_AS_USER = "button:has-text('Войти как пользователь')"

    URL = 'https://user:senlatest@regoffice.senla.eu'

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.URL)

    def click_login_as_user(self):
        self.page.locator(self.BTN_LOGIN_AS_USER).click()


