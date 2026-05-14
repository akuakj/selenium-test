from pydantic import BaseModel
from typing import Optional


class ApplicationResponse(BaseModel):
    applicantid: int
    applicationid: int
    citizenid: int
    dateofapplication: str
    kindofapplication: str
    statusofapplication: int
    staffid: Optional[int] = None