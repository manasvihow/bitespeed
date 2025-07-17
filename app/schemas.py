from typing import List, Optional
from sqlmodel import SQLModel

class IdentifyRequest(SQLModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None

class ContactResponse(SQLModel):
    primaryContactId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]

class IdentifyResponse(SQLModel):
    contact: ContactResponse