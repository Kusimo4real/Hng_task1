from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
import uuid

class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: Optional[str] = None
    class Config:
        from_attributes = True 
        orm_mode =True

class UserCreate(UserBase):
    password: str

class UserRespons(UserBase):
    userId: uuid.UUID

class User(UserBase):
    data: Dict
    message: str
    status: str
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str

class OrganisationBase(BaseModel):
    name: str
    description: Optional[str] = None

class OrganisationCreate(OrganisationBase):
    pass

class Organisation(OrganisationBase):
    orgId: str

    class Config:
        orm_mode = True
        from_attributes = True 


# List of organisations response schema
class OrganisationList(BaseModel):
    organisations: list[Organisation]

class AddUserOrgan(BaseModel):
    userId: str
