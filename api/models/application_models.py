from pydantic import BaseModel
from typing import Optional, List

class GetApplicationsResponseData(BaseModel):
    applicantid: Optional[int] = None
    applicationid: Optional[int] = None
    citizenid: Optional[int] = None
    dateofapplication: Optional[str] = None
    kindofapplication: Optional[str] = None
    statusofapplication: Optional[str] = None
    staffid: Optional[int] = None

class GetApplicationsResponse(BaseModel):
    total: Optional[int] = None
    data: List[GetApplicationsResponseData]
    requestsId: Optional[str] = None

class GetApplStatus(BaseModel):
    applicationId : Optional[int]

class GetApplStatusResponseData(BaseModel):
    dateofapplication: Optional[str]
    kindofapplication: Optional[str]
    statusofapplication: Optional[str]

class GetApplStatusResponse(BaseModel):
    data: GetApplStatusResponseData
    requestId: Optional[str]

class ResponseNotFound(BaseModel):
    code: Optional[int]
    message: Optional[str]