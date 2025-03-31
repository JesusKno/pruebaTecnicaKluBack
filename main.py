from fastapi import FastAPI
from routes import transaccionesRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#Routers
app.include_router(transaccionesRouter.router)


#permisos cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/")
def read():

    return {'Hola Mundo'}
