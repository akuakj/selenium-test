from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Locators:
    USER_LOGIN = (By.XPATH, "//button[contains(text(), 'Войти как пользователь')]")

    MARRIAGE_SERVICE = (By.XPATH, "//button[contains(text(), 'Регистрация брака')]")

    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Далее')]")
    FINISH_BUTTON = (By.XPATH, "//button[contains(text(), 'Завершить')]")

    SURNAME_USER = (By.XPATH, "//input[@placeholder='Введите фамилию (минимум 2 символа)']")
    NAME_USER = (By.XPATH, "//input[@placeholder='Введите имя (минимум 2 символа)']")
    MIDNAME_USER = (By.XPATH, "//input[@placeholder='Введите отчество (минимум 5 символов)']")
    PHONE_USER = (By.XPATH, "//input[@placeholder='Введите номер телефона (не более 11 символов)']")
    PASSPORT_USER = (By.XPATH, "//input[@placeholder='Введите номер паспорта (не более 8 символов)']")
    ADDRESS_USER = (By.XPATH, "//input[@placeholder='Введите адрес прописки']")

    SURNAME_CITIZEN = (By.XPATH, "(//input[@maxlength='100'])[1]")
    NAME_CITIZEN = (By.XPATH, "(//input[@maxlength='100'])[2]")
    MIDNAME_CITIZEN = (By.XPATH, "(//input[@maxlength='100'])[3]")
    DATE_CITIZEN = (By.XPATH, "//input[@type='date']")
    PASSPORT_CITIZEN = (By.XPATH, "//input[@maxlength='8']")
    GENDER_CITIZEN = (By.XPATH, "//input[@maxlength='4']")
    ADDRESS_CITIZEN = (By.XPATH, "//input[@placeholder='Введите адрес прописки']")

    MARRIAGE_DATE = (By.XPATH, "(//input[@type='date'])[1]")
    NEW_SURNAME = (By.XPATH, "(//input[@maxlength='50'])[1]")
    SPOUSE_SURNAME = (By.XPATH, "(//input[@maxlength='50'])[2]")
    SPOUSE_NAME = (By.XPATH, "(//input[@maxlength='20'])[1]")
    SPOUSE_MIDNAME = (By.XPATH, "(//input[@maxlength='20'])[2]")
    SPOUSE_BIRTHDATE = (By.XPATH, "(//input[@type='date'])[2]")
    SPOUSE_PASSPORT = (By.XPATH, "//input[@maxlength='8']")

    SUCCESS_TEXT = (By.XPATH, "//*[contains(text(), 'Спасибо за обращение')]")
    STATUS_TEXT = (By.XPATH, "//*[contains(text(), 'Статус заявки')]")

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("https://user:senlatest@regoffice.senla.eu")
print("Авторизация: успешно")

user_btn = wait.until(EC.element_to_be_clickable(Locators.USER_LOGIN))
user_btn.click()
print("Выбрано: 'войти как пользователь'")
time.sleep(1)

# ── Шаг 1: Данные заявителя
try:
    wait.until(EC.presence_of_element_located(Locators.SURNAME_USER)).send_keys("Ivanov")
    driver.find_element(*Locators.NAME_USER).send_keys('Ivan')
    driver.find_element(*Locators.MIDNAME_USER).send_keys('Ivanovich')
    driver.find_element(*Locators.PHONE_USER).send_keys('1234567890')
    driver.find_element(*Locators.PASSPORT_USER).send_keys('AB123456')
    driver.find_element(*Locators.ADDRESS_USER).send_keys('Брест, улица Машерова 12')
    print("Шаг 1: форма заявителя заполнена")

    driver.find_element(*Locators.NEXT_BUTTON).click()
    print('Шаг 1: нажата кнопка "Далее"')

    time.sleep(1)

except Exception as e:
    print(f"Ошибка на шаге 1: {e}")


# ── Шаг 2: Выбор услуги
try:
    marriage_btn = wait.until(EC.element_to_be_clickable(Locators.MARRIAGE_SERVICE))
    marriage_btn.click()
    print("Шаг 2: выбрана услуга 'Регистрация брака'")

    time.sleep(1)

except Exception as e:
    print(f"Ошибка на шаге 2: {e}")


# ─ Шаг 3: Форма "Данные гражданина"
try:
    wait.until(EC.presence_of_element_located(Locators.SURNAME_CITIZEN)).send_keys("Ivanov")
    driver.find_element(*Locators.NAME_CITIZEN).send_keys("Ivan")
    driver.find_element(*Locators.MIDNAME_CITIZEN).send_keys("Ivanovich")
    driver.find_element(*Locators.DATE_CITIZEN).send_keys("11.04.1999")
    driver.find_element(*Locators.PASSPORT_CITIZEN).send_keys("AB123456")
    driver.find_element(*Locators.GENDER_CITIZEN).send_keys("M")
    driver.find_element(*Locators.ADDRESS_CITIZEN).send_keys("Брест, улица Машерова 12")
    print("Шаг 3: данные гражданина заполнены")

    driver.find_element(*Locators.NEXT_BUTTON).click()
    print('Шаг 3: нажата кнопка "Далее"')

    time.sleep(1)

except Exception as e:
    print(f"Ошибка на шаге 3: {e}")


# ── Шаг 4: Данные услуги
try:
    wait.until(EC.presence_of_element_located(Locators.MARRIAGE_DATE)).send_keys("01072026")
    driver.find_element(*Locators.NEW_SURNAME).send_keys("Ivanova")
    driver.find_element(*Locators.SPOUSE_SURNAME).send_keys("Ivanova")
    driver.find_element(*Locators.SPOUSE_NAME).send_keys("Nastya")
    driver.find_element(*Locators.SPOUSE_MIDNAME).send_keys("Petrovna")
    driver.find_element(*Locators.SPOUSE_BIRTHDATE).send_keys("20031993")
    driver.find_element(*Locators.SPOUSE_PASSPORT).send_keys("АВ87654")
    print("Шаг 4: данные услуги заполнены")

    driver.find_element(*Locators.FINISH_BUTTON).click()
    print('Шаг 4: нажата кнопка "Завершить"')

    time.sleep(2)

except Exception as e:
    print(f"Ошибка на шаге 4: {e}")


try:
    success = wait.until(EC.presence_of_element_located(Locators.SUCCESS_TEXT))
    status = driver.find_element(*Locators.STATUS_TEXT)
    print("\n" + "="*50)
    print("✅ ТЕСТ ПРОЙДЕН!")
    print(success.text)
    print(status.text)
    print("="*50)

except Exception as e:
    print(f"Финальный экран не появился: {e}")


driver.quit()