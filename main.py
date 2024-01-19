from fastapi import FastAPI, HTTPException
from database import get_all_customer
from database import save_customer
from database import validate_exist_email
from database import get_one_customer
from database import remove_customer
from database import update_customer
from models import Customer, UpdateCustomer


app = FastAPI()
app.title = "Base de Datos Clientes"
app.version = "0.0.1"


# pipenv run uvicorn main:app --reload

# --- WELCOME --- #
# --- 0.0.- GET Request: Ruta que Devuelva un Mensaje de Bienvenida  --- #
@app.get('/api/v1', tags=['Welcome'])
async def welcome():
    return {'message': '🤟🏻 Bienvenido a Mi Primera API RESTful con FastAPI'}


# --- CUSTOMERS --- #
# --- 1.1.- GET Reguest: Ruta que Devuelva Todos los Clientes | Conectado a MongoDB  --- #
@app.get('/api/v1/customers', response_model=list, tags=['Customers'])
async def index_customers():
    customers = await get_all_customer()

    return customers


# --- CUSTOMER --- #
# --- 2.1.- GET Reguest: Ruta que Devuelva un Cliente a través de su ID | Conectado a MongoDB  --- #
@app.get('/api/v1/customers/{id}', response_model=Customer, tags=['Customer'])
async def show_customers(id: str):
    customer = await get_one_customer(id)

    if customer:
        return Customer(**customer)
    else:
        raise HTTPException(404, f"Cliente con el ID {id} No ha Sido Encontrado 😰")


# --- 2.2.- POST Requests: Ruta que nos permita Crear un Nuevo Cliente | Conectado a MongoDB --- #
@app.post('/api/v1/customers', response_model=Customer, tags=['Customer'])
async def create_customers(customer: Customer):

    email_found = await validate_exist_email(customer.email)

    if email_found:
        raise HTTPException(409, '⚠️ Ups, el correo ya existe')
    else:
        response = await save_customer(customer.dict())

        if response:
            return Customer(**response)

        else:
            raise HTTPException(400, '⚠️ Ups, algo salio mal 🤯')


# --- 2.3.- PUT Requests: Ruta que nos permita Actualizar un Nuevo Cliente | Conectado a MongoDB --- #
@app.put('/api/v1/customers/{id}', response_model=Customer, tags=['Customer'])
async def update_customers(id: str, data: UpdateCustomer):
    response = await update_customer(id, data)

    if response:
        return Customer(**response)

    else:
        raise HTTPException(404, f"Cliente con el ID {id} No ha Sido Encontrado 😰")


# --- 2.4.- DELETE Requests: Ruta que nos permita Eliminar un Nuevo Cliente | Conectado a MongoDB --- #
@app.delete('/api/v1/customers/{id}', tags=['Customer'])
async def delete_customers(id: str):

    response = await remove_customer(id)

    if response:
        return f"El Cliente con el ID {id} Ha sido Eliminado Correctamente "

    else:
        raise HTTPException(404, f"Cliente con el ID {id} ya ha sido eliminado ❌")

