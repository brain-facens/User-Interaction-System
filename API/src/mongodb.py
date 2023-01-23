from pymongo import MongoClient
from bson.objectid import ObjectId

with open('access/creds.txt') as docs:
    creds = docs.readlines()
    creds[0] = creds[0].removesuffix('\n')
    docs.close()
client = MongoClient(
    f'mongodb+srv://{creds[0]}:{creds[1]}@cluster0.wmzqvkh.mongodb.net/?retryWrites=true&w=majority')
database = client.mongotuts
collection = database.get_collection('people')

def person_helper(person) -> dict:
    return {
        "id": str(person['_id']),
        "nome": person['nome'],
        "horarios": person['horarios'],
        "emocoes": person['emocoes'],
        "setor": person['setor'],
        "imagem": person['imagem'],
    }

async def retrieve_people():
    # try to do it in one line later
    people = []
    for person in collection.find({}):
        people.append(person_helper(person))
    return people

async def retrieve_person(field: str, val: str, id: str = None):
    if not id:
        person = collection.find_one({field: val})
    else:
        person = collection.find_one({'_id': ObjectId(id)})
    if person:
        return person_helper(person)

async def add_person(data: dict) -> dict:
    person = collection.insert_one(data)
    new_person = collection.find_one({'_id': person.inserted_id})
    return person_helper(new_person)

async def update_person(field: str, val: str, data: dict):
    if len(data) < 1:
        return False
    person = collection.find_one({field: val})
    if person:
        updated_person = collection.update_one({field: val}, {"$set": data})
        if updated_person:
            return True
        return False

async def delete_person(field: str, val: str):
    person = collection.find_one({field: val})
    if person:
        collection.delete_one({field: val})
        return True

def close_client(self):
    self.client.close()
