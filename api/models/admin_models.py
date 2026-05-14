from pydantic import BaseModel
from typing import Optional

class AdminRequest(BaseModel):
    personalLastName: Optional[str]
    personalFirstName: Optional[str]
    personalMiddleName: Optional[str]
    personalPhoneNumber: Optional[str]
    personalNumberOfPassport: Optional[str]
    dateofbirth: Optional[str]

class AdminResponseData(BaseModel):
    staffid: Optional[int]

class AdminResponse(BaseModel):
    data: AdminResponseData
    requestId: Optional[str]

class AdminBadRequest(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None

class ProcessRequest(BaseModel):
    applId: Optional[int]
    staffid: Optional[int]
    action: Optional[str]

class ProcessResponseData(BaseModel):
    applicantid: Optional[int]
    applicationid: Optional[int]
    citizenid: Optional[int]
    dateofapplication: Optional[str]
    kindofapplication: Optional[str]
    statusofapplication: Optional[str]
    staffid: Optional[int]
    channel: Optional[str] = None
    image: Optional[str] = None

class ProcessResponse(BaseModel):
    data: ProcessResponseData
    requestId: Optional[str]

