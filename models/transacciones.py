from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, completed, failed
    stripe_payment_intent_id = Column(String, nullable=True)
    stripe_client_secret = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
