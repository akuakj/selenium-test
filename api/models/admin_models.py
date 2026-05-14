from pydantic import BaseModel
from typing import Optional

class AdminRequest(BaseModel):
    personalLastName: Optional[str] = None
    personalFirstName: Optional[str] = None
    personalMiddleName: Optional[str] = None
    personalPhoneNumber: Optional[str] = None
    personalNumberOfPassport: Optional[str] = None
    dateofbirth: Optional[str] = None

class AdminResponseData(BaseModel):
    staffid: int

class AdminResponse(BaseModel):
    data: AdminResponseData
    requestId: str

class ProcessRequest(BaseModel):
    applId: int
    staffid: int
    action: str


class ProcessResponse(BaseModel):
    applicantid: int
    applicationid: int
    citizenid: int
    dateofapplication: str
    kindofapplication: str
    statusofapplication: int
    staffid: int


class AdminBadRequest(BaseModel):
    code: str
    message: str

