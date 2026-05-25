from pydantic import BaseModel
from typing import Optional


class UserRequest(BaseModel):
    mode: Optional[str] = None
    personalLastName: Optional[str] = None
    personalFirstName: Optional[str] = None
    personalMiddleName: Optional[str] = None
    personalPhoneNumber: Optional[str] = None
    personalNumberOfPassport: Optional[str] = None
    personalAddress: Optional[str] = None
    citizenLastName: Optional[str] = None
    citizenFirstName: Optional[str] = None
    citizenMiddleName: Optional[str] = None
    citizenBirthDate: Optional[str] = None
    citizenNumberOfPassport: Optional[str] = None
    citizenGender: Optional[str] = None
    citizenAddress: Optional[str] = None
    dateOfMarriage: Optional[str] = None
    newLastName: Optional[str] = None
    anotherPersonLastName: Optional[str] = None
    anotherPersonFirstName: Optional[str] = None
    anotherPersonMiddleName: Optional[str] = None
    birth_of_anotoherPerson: Optional[str] = None
    anotherPersonPassport: Optional[str] = None
    birth_place: Optional[str] = None
    birth_mother: Optional[str] = None
    birth_father: Optional[str] = None
    birth_grandpa: Optional[str] = None
    birth_grandma: Optional[str] = None
    death_dateOfDeath: Optional[str] = None
    death_placeOfDeath: Optional[str] = None

class UserResponseData(BaseModel):
    applicantid: Optional[int] = None
    applicationid: Optional[int] = None
    citizenid: Optional[int] = None
    merrigecertificateid: Optional[int] = None
    birthcertificateid: Optional[int] = None

class UserResponse(BaseModel):
    data: UserResponseData
    requestId: Optional[str] = None

class UserBadRequest(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None

