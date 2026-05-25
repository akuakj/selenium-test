from enum import Enum

class ApplicationStatus(Enum):
    APPROVED = 'Одобрена'
    REJECTED = 'Отклонена'
    PENDING = 'На рассмотрении'

class ServiceType(Enum):
    MARRIAGE = 'Регистрация брака'
    BIRTH = 'Регистрация рождения'

class Gender(Enum):
    MALE_FULL = 'муж'
    FEMALE_FULL = 'жен'
    MALE_SHORT = 'м'
    FEMALE_SHORT = 'ж'

class StatusOfApplicationAPI(Enum):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    UNDER_CONSIDERATION = 'under consideration'