from motor.motor_asyncio import AsyncIOMotorClient
from models import Customer, UpdateCustomer
from bson.objectid import ObjectId
from models import PyObjectId

client = AsyncIOMotorClient('mongodb://localhost:27017')

database = client.TestAPI_DB
collection = database.customers


# --- CUSTOMERS --- #
# --- 1.1.- Método que devuelve todos los clientes de la Base de Datos  --- #
async def get_all_customer():
    customers = []
    records = collection.find({})
    async for document in records:
        customers.append(Customer(**document))
    return customers


# --- CUSTOMER --- #
# --- 2.1.- GET Reguest: Método que devuelve un cliente a través de su ID en la Base de Datos  --- #
async def get_one_customer(id):
    if ObjectId.is_valid(id):
        record = await collection.find_one({"_id": ObjectId(id)})
    else:
        record = False

    return record


# --- 2.2.- POST Requests: Método que nos permitirá saber si es que ya existe un usuario con el mismo correo en la base de datos --- #
async def validate_exist_email(email: str):
    record = await collection.find_one({'email': email})
    return record


# --- 2.2.- POST Requests: Método que nos permite Crear Nuevos Clientes y Almacenarlos en la Base de Datos  --- #
async def save_customer(customer):
    record = await collection.insert_one(customer)
    record_id = await collection.find_one({'_id': record.inserted_id})
    return record_id


# --- 2.3.- PUT Requests: Método que actualiza los atributos cliente a través de su ID en la Base de Datos  --- #
async def update_customer(id: str, data: UpdateCustomer):

    record_clean = {k: v for k, v in data.dict().items() if v is not None}

    if ObjectId.is_valid(id):
        await collection.update_one({"_id": ObjectId(id)}, {"$set": record_clean})
        record = await collection.find_one({"_id": ObjectId(id)})
    else:
        record = False

    return record


# --- 2.4.- DELETE Requests: Método elimina un cliente a través de su ID en la Base de Datos  --- #
async def remove_customer(id: str) -> bool:

    if ObjectId.is_valid(id):
        record = await collection.find_one({"_id": ObjectId(id)})

        if record:
            await collection.delete_one({"_id": record['_id']})
            return True
        else:
            return False

    else:
        return False



