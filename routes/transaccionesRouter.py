from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import uuid
import os
import stripe
from config.db import SessionLocal
from models.transacciones import Transaction
from schemas.transactionesSchemas import TransactionCreate, TransactionResponse

# Cargar las variables de ambiente
load_dotenv()

# Configurar Stripe con la clave secreta obtenida desde el archivo .env
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter()

# Dependencia para la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para integrar con Stripe mediante PaymentIntent
def process_payment(transaction: Transaction) -> dict:
    try:
        # Convertir el monto a centavos
        amount_in_cents = int(transaction.amount * 100)
        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=transaction.currency,
            description=f"Payment for transaction {transaction.id}",
            metadata={
                "customer_email": transaction.customer_email,
                "customer_name": transaction.customer_name
            }
        )
        return intent
    except Exception as e:
        raise Exception(f"Error creating PaymentIntent: {str(e)}")

# 1. Iniciar una transacción (POST)
@router.post("/transactions/")
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db)
):
    # Crear y guardar la transacción inicialmente con status "pending"
    transaction = Transaction(
        amount=data.amount,
        currency=data.currency,
        customer_email=data.customer_email,
        customer_name=data.customer_name,
        status="pending"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    try:
        # Procesar el pago creando un PaymentIntent en Stripe
        response = process_payment(transaction)
        # Almacenar los datos de Stripe en la transacción
        transaction.stripe_payment_intent_id = response.get("id")
        transaction.stripe_client_secret = response.get("client_secret")
        # El estado permanece "pending" hasta la confirmación del pago
        transaction.status = "pending"
        db.commit()
        db.refresh(transaction)
    except Exception as e:
        transaction.status = "failed"
        db.commit()
        raise HTTPException(status_code=400, detail=str(e))
    
    return transaction

# 2. Obtener estado de una transacción (GET)
@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: uuid.UUID, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# 3. Listar transacciones (GET)
@router.get("/transactions/")
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

