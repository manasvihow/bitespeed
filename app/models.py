from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phoneNumber: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None, index=True)
    linkedId: Optional[int] = Field(default=None, foreign_key="contact.id")
    linkPrecedence: str = Field(index=True)  # "primary" or "secondary"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    deletedAt: Optional[datetime] = Field(default=None)