from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from src.Models.person import PersonSchema, UpdatePersonModel, ResponseModel, ErrorResponseModel
from src.mongodb import add_person, delete_person, retrieve_person, retrieve_people, update_person, person_helper

router = APIRouter()

@router.get('/')
async def find_all():
    people = await retrieve_people()
    if len(people) > 0:
        return ResponseModel(people, 'Registered people data retrieved.')
    return ResponseModel(people, 'Empty list retrieved.')

@router.post('/', response_description='Add new Person')
async def create_person(person: PersonSchema = Body(...)):
    person = jsonable_encoder(person)
    new_person = await add_person(person)
    return ResponseModel(new_person, 'Person added.')

@router.get('/{nome}')
async def retrieve_person_data(nome: str):
    person = await retrieve_person('nome', nome)
    if person:
        return ResponseModel(person, 'Person data retrieved.')

@router.put('/{nome}')
async def update_person_data(nome: str, req: UpdatePersonModel = Body(...)):
    req = {k:v for k,v in req.dict().items() if v is not None}
    updated_person = await update_person('nome', nome, req)
    if updated_person:
        return ResponseModel(f"{nome} update is successfull", 'Person updated successfully')
    return ErrorResponseModel('An error occurred', 404, 'There was an error updating person data.')

@router.delete('/{nome}')
async def delete_person_data(nome: str):
    deleted_person = await delete_person('nome', nome)
    if deleted_person:
        return ResponseModel(f'{nome} deleted from database.', 'Person deleted successfully')
    return ErrorResponseModel('An error occurred', 404, f'{nome} not found in db')
