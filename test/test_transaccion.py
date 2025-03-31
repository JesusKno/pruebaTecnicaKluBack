import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("sys.path[0]:", sys.path[0])

from main import app



# Instanciar el cliente de FastAPI para realizar las peticiones en los tests.
client = TestClient(app)

# Función dummy para simular la respuesta de Stripe en process_payment.
def dummy_process_payment(transaction):
    # Simula una respuesta exitosa de Stripe.
    return {
        "id": "pi_dummy_123",
        "client_secret": "cs_dummy_456",
        "approved": True
    }

# Test para crear una transacción exitosa
def test_create_transaction_success(monkeypatch):
    # Reemplaza la función real process_payment por la dummy.
    monkeypatch.setattr("routes.transaccionesRouter.process_payment", dummy_process_payment)
    
    payload = {
        "amount": 10.0,
        "currency": "USD",
        "customer_email": "test@example.com",
        "customer_name": "Test User"
    }
    
    response = client.post("/transactions/", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    # Verifica que los datos se retornan correctamente.
    assert data["amount"] == 10.0
    assert data["currency"] == "USD"
    assert data["customer_email"] == "test@example.com"
    assert data["customer_name"] == "Test User"
    # Verifica que se han asignado los datos simulados de Stripe.
    assert data["stripe_payment_intent_id"] == "pi_dummy_123"
    assert data["stripe_client_secret"] == "cs_dummy_456"
    # El estado se mantiene "pending" hasta que se confirme el pago.
    assert data["status"] == "pending"

# Test para validar errores de validación: monto negativo.
def test_create_transaction_invalid_amount():
    payload = {
        "amount": -5.0,
        "currency": "USD",
        "customer_email": "test@example.com",
        "customer_name": "Test User"
    }
    response = client.post("/transactions/", json=payload)
    # FastAPI debe devolver un error de validación (422 Unprocessable Entity).
    assert response.status_code == 422

# Test para obtener una transacción por ID.
def test_get_transaction(monkeypatch):
    # Primero crea una transacción usando el monkeypatch para Stripe.
    monkeypatch.setattr("routes.transaccionesRouter.process_payment", dummy_process_payment)
    
    payload = {
        "amount": 15.0,
        "currency": "USD",
        "customer_email": "get_test@example.com",
        "customer_name": "Get Test"
    }
    create_response = client.post("/transactions/", json=payload)
    assert create_response.status_code == 200, create_response.text
    created_data = create_response.json()
    transaction_id = created_data["id"]
    
    # Realiza la petición GET para obtener la transacción.
    get_response = client.get(f"/transactions/{transaction_id}")
    assert get_response.status_code == 200, get_response.text
    data_get = get_response.json()
    assert data_get["id"] == transaction_id
    assert data_get["customer_email"] == "get_test@example.com"

# Test para listar todas las transacciones.
def test_list_transactions(monkeypatch):
    # Crea dos transacciones para asegurarse de que haya varias en la lista.
    monkeypatch.setattr("routes.transaccionesRouter.process_payment", dummy_process_payment)
    
    payload = {
        "amount": 20.0,
        "currency": "USD",
        "customer_email": "list_test@example.com",
        "customer_name": "List Test"
    }
    response1 = client.post("/transactions/", json=payload)
    response2 = client.post("/transactions/", json=payload)
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    list_response = client.get("/transactions/")
    assert list_response.status_code == 200
    data_list = list_response.json()
  
    assert isinstance(data_list, list)
    assert len(data_list) >= 2
