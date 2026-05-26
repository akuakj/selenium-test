from playwright.sync_api import Page


class StatusPage:
    TEXT_THX = "text=Спасибо за обращение!"
    TEXT_STATUS = "text=отправлена на рассмотрение"

    BTN_REFRESH = "button:has-text('Обновить')"
    BTN_NEW_APPLICATION = "button:has-text('Создать новую заявку')"
    BTN_CLOSE = "button:has-text('Закрыть')"

    def __init__(self, page: Page):
        self.page = page

    def get_thx_text(self):
        return self.page.locator(self.TEXT_THX)

    def get_status_text(self):
        return self.page.locator(self.TEXT_STATUS)

    def click_refresh(self):
        self.page.locator(self.BTN_REFRESH).click()

    def click_new_application(self):
        self.page.locator(self.BTN_NEW_APPLICATION).click()

    def click_close(self):
        self.page.locator(self.BTN_CLOSE).click()