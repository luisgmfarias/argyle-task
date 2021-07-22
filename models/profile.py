from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Address(BaseModel):
    line1: Optional[str]
    line2: Optional[str]
    city: str
    state: str
    postal_code: Optional[str]
    country: str


class Profile(BaseModel):
    id: int
    account: str
    employer: str
    created_at: datetime
    updated_at: Optional[datetime]
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    email: str
    phone_number: int
    birth_date: Optional[datetime]
    picture_url: Optional[str]
    address: Address
    ssn: Optional[int]
    marital_status: Optional[str]
    gender: Optional[str]
    metadata: dict = {}
