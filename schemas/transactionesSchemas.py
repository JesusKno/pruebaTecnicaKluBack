from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="El monto debe ser mayor a 0")
    currency: str
    customer_email: EmailStr
    customer_name: str = Field(...,min_length=1)

class TransactionResponse(TransactionCreate):
    id: UUID
    status: str
    stripe_payment_intent_id: str | None = None
    stripe_client_secret: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True
