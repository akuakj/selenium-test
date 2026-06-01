import allure

class DBAsserts:

    def __init__(self, db_client):
        self.db = db_client

    @allure.step('Проверить данные заявителя в БД')
    def check_applicant_matches_payload(self, applicant_id: int, payload):
        db_applicant = self.db.get_applicant_by_id(applicant_id)

        assert payload.personalFirstName == db_applicant.name, (
            f"Имя: ожидалось '{payload.personalFirstName}', в БД '{db_applicant.name}'"
        )
        assert payload.personalLastName == db_applicant.surname, (
            f"Фамилия: ожидалось '{payload.personalLastName}', в БД '{db_applicant.surname}'"
        )
        assert payload.personalMiddleName == db_applicant.middlename, (
            f"Отчество: ожидалось '{payload.personalMiddleName}', в БД '{db_applicant.middlename}'"
        )
        assert payload.personalNumberOfPassport == db_applicant.passportnumber, (
            f"Номер паспорта: ожидался '{payload.personalNumberOfPassport}', в БД '{db_applicant.passportnumber}'"
        )
        assert payload.personalPhoneNumber == db_applicant.phonenumber, (
            f"Телефон: ожидался '{payload.personalPhoneNumber}', в БД '{db_applicant.phonenumber}'"
        )
        assert payload.personalAddress == db_applicant.registration_address, (
            f"Адрес: ожидался '{payload.personalAddress}', в БД '{db_applicant.registration_address}'"
        )


    @allure.step("Проверить данные гражданина в БД")
    def check_citizen_matches_payload(self, citizen_id: int, payload):
        db_citizen = self.db.get_citizen_by_id(citizen_id)

        assert payload.citizenLastName == db_citizen.surname, (
            f"Фамилия: ожидалось '{payload.citizenLastName}', в БД '{db_citizen.surname}'"
        )
        assert payload.citizenFirstName == db_citizen.name, (
            f"Имя: ожидалось '{payload.citizenFirstName}', в БД '{db_citizen.name}'"
        )
        assert payload.citizenMiddleName == db_citizen.middlename, (
            f"Отчество: ожидалось '{payload.citizenMiddleName}', в БД '{db_citizen.middlename}'"
        )
        assert payload.citizenNumberOfPassport == db_citizen.passportnumber, (
            f"Паспорт: ожидался '{payload.citizenNumberOfPassport}', в БД '{db_citizen.passportnumber}'"
        )
        assert payload.citizenAddress == db_citizen.registration_address, (
            f"Адрес: ожидался '{payload.citizenAddress}', в БД '{db_citizen.registration_address}'"
        )


    @allure.step("Проверить данные администратора в БД")
    def check_admin_matches_payload(self, staff_id: int, payload):
        db_staff = self.db.get_staff_by_id(staff_id)

        assert payload.personalLastName == db_staff.surname, (
            f"Фамилия: ожидалась '{payload.personalLastName}', в БД '{db_staff.surname}'"
        )
        assert payload.personalFirstName == db_staff.name, (
            f"Имя: ожидалось '{payload.personalFirstName}', в БД '{db_staff.name}'"
        )
        assert payload.personalMiddleName == db_staff.middlename, (
            f"Отчество: ожидалось '{payload.personalMiddleName}', в БД '{db_staff.middlename}'"
        )
        assert payload.personalPhoneNumber == db_staff.phonenumber, (
            f"Телефон: ожидался '{payload.personalPhoneNumber}', в БД '{db_staff.phonenumber}'"
        )
        assert payload.personalNumberOfPassport == db_staff.passportnumber, (
            f"Паспорт: ожидался '{payload.personalNumberOfPassport}', в БД '{db_staff.passportnumber}'"
        )
        assert payload.dateofbirth == str(db_staff.dateofbirth), (
            f"Дата рождения: ожидалась '{payload.dateofbirth}', в БД '{db_staff.dateofbirth}'"
        )

    @allure.step("Проверить статус заявки в БД")
    def check_application_status(self, application_id: int, expected_status: str):
        db_status = self.db.get_application_status(application_id)

        assert db_status == expected_status, (
            f"Статус в БД: '{db_status}', ожидался: '{expected_status}'"
        )

    @allure.step("Проверить staffid привязан к заявке в БД")
    def check_application_staff(self, application_id: int, expected_staff_id: int):
        db_application = self.db.get_application_by_id(application_id)

        assert db_application.staffid == expected_staff_id, (
            f"staffid в БД: {db_application.staffid}, ожидался: {expected_staff_id}"
        )