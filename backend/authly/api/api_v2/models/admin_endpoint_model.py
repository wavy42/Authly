from typing import List, Optional
from pydantic import BaseModel, EmailStr


class CreateAdminReponse(BaseModel):
    id: str
    username: str
    email: EmailStr


class AdminAccount(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    role: List[str]
    geo_location: str  # for timezone :)
    bubble: List
    settings: List


class AllAdminAccounts(BaseModel):
    data: List[AdminAccount]


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateBubbleResponse(BaseModel):
    id: str
    name: str
