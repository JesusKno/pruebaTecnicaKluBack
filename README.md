Prueba Técnica KluBack
Proyecto de prueba técnica para desarrollar una aplicación backend de procesamiento de pagos utilizando FastAPI, SQLAlchemy y Alembic, con integración a Stripe.

Tabla de Contenidos
Instalación

Configuración

Ejecución

Migraciones de Base de Datos

Endpoints de la API

Pruebas

Variables de Entorno

Tecnologías Utilizadas

Instalación
Clonar el repositorio:

git clone https://github.com/tu_usuario/pruebaTecnicaKluBack.git
cd pruebaTecnicaKluBack
Crear y activar el entorno virtual:

En Windows:

python -m venv env
env\Scripts\activate

En macOS/Linux:

python3 -m venv env
source env/bin/activate
Instalar las dependencias:

pip install -r requirements.txt

Configuración
Variables de Entorno:
Crea un archivo .env en la raíz del proyecto con el siguiente contenido (ajusta según tus datos):

Se anexa .env.example con las credenciales que se neeceensitan

env

# Base de datos (ejemplo para PostgreSQL)

DB_URL=postgresql://usuario:contraseña@localhost:5432/payments_app

# Clave secreta de Stripe en modo de prueba

STRIPE_SECRET_KEY=sk_test_XXXXXXXXXXXXXXXXXXXXXXXX
Configuración de Alembic:
Asegúrate de que el archivo alembic/env.py esté configurado para leer la variable DB_URL y actualizar la URL de conexión. Consulta la sección de Migraciones para más detalles.

Ejecución

Para iniciar la aplicación, ejecuta:

uvicorn main:app --reload
La aplicación se levantará en http://localhost:8000.
Accede a /docs para ver la documentación interactiva generada automáticamente por FastAPI.

Migraciones de Base de Datos
El proyecto utiliza Alembic para gestionar las migraciones.

Generar una migración:
(EEjeemplo)
alembic revision --autogenerate -m "Agregar columnas stripe_payment_intent_id y stripe_client_secret"

Aplicar migraciones:

alembic upgrade head

Endpoints de la API
La API expone los siguientes endpoints:

POST /transactions/
Crea una nueva transacción y genera un PaymentIntent en Stripe.
Cuerpo de la solicitud (JSON):

json
{
"amount": 10.0,
"currency": "USD",
"customer_email": "test@example.com",
"customer_name": "Test User"
}
Respuesta exitosa (200):

json
{
"id": "uuid-de-la-transacción",
"amount": 10.0,
"currency": "USD",
"customer_email": "test@example.com",
"customer_name": "Test User",
"status": "pending",
"stripe_payment_intent_id": "pi_xxx",
"stripe_client_secret": "cs_xxx",
"created_at": "2023-03-15T12:00:00"
}
GET /transactions/{transaction_id}
Devuelve la información de una transacción específica.

GET /transactions/
Lista todas las transacciones registradas.

Explora y prueba estos endpoints en http://localhost:8000/docs.

Pruebas
El proyecto incluye tests con Pytest.
Para ejecutar los tests:

Asegúrate de que el entorno virtual esté activo.

Desde la raíz del proyecto, ejecuta:

pytest
Para obtener un reporte de cobertura de código (si tienes instalado pytest-cov):

pytest --cov=.

Variables de Entorno
Configura las siguientes variables en el archivo .env:

DB_URL: URL de conexión a la base de datos (por ejemplo, para PostgreSQL:
postgresql://usuario:contraseña@localhost:5432/payments_app)

STRIPE_SECRET_KEY: Clave secreta de Stripe (modo de prueba).

Tecnologías Utilizadas
Backend: FastAPI, SQLAlchemy, Alembic

Pagos: Stripe

Validación: Pydantic

Testing: Pytest, FastAPI TestClient

Base de Datos: PostgreSQL (o SQLite en desarrollo)
