from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class Contact(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    metadata: dict = {}
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True
            }
        }
