import os
import secrets
from typing import Annotated

import motor.motor_asyncio
from bson import ObjectId
from pymongo import ReturnDocument
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Body, HTTPException, status, Depends

from app.models import PersonModel, UpdatePersonModel, PersonCollection

security = HTTPBasic()


def get_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    user = os.environ.get('API_USER')
    password = os.environ.get('API_PASSWORD')
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(user, encoding='utf-8')
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = bytes(password, encoding='utf-8')
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


app = FastAPI(
    title="Persons API",
    summary="A sample application to add and retrieve basic information about Persons",
    dependencies=[Depends(get_auth)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_db_connection_string = os.environ.get('MDB_CONN_STR')

client = motor.motor_asyncio.AsyncIOMotorClient(
    # "mongodb+srv://test:kdrsRIjfNrNYYTX5@personcrud.w9kvvra.mongodb.net/?retryWrites=true&w=majority"
    mongo_db_connection_string
)
db = client.data
person_collection = db.get_collection("person")


@app.post(
    "/persons/",
    response_description="Add new person",
    response_model=PersonModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_person(person: PersonModel = Body(...)):
    new_person = await person_collection.insert_one(
        person.model_dump(by_alias=True, exclude=["id"])
    )
    created_person = await person_collection.find_one(
        {"_id": new_person.inserted_id}
    )
    return created_person


@app.get(
    "/persons/",
    response_description="List all persons",
    response_model=PersonCollection,
    response_model_by_alias=False,
)
async def list_persons():
    return PersonCollection(persons=await person_collection.find().to_list(1000))


@app.get(
    "/persons/{id}",
    response_description="Get a single person",
    response_model=PersonModel,
    response_model_by_alias=False,
)
async def show_person(id: str):
    if (
            person := await person_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return person

    raise HTTPException(status_code=404, detail=f"person {id} not found")


@app.put(
    "/persons/{id}",
    response_description="Update a person",
    response_model=PersonModel,
    response_model_by_alias=False,
)
async def update_person(id: str, person: UpdatePersonModel = Body(...)):
    person = {
        k: v for k, v in person.model_dump(by_alias=True).items() if v is not None
    }

    if len(person) >= 1:
        update_result = await person_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": person},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"person {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_person := await person_collection.find_one({"_id": id})) is not None:
        return existing_person

    raise HTTPException(status_code=404, detail=f"person {id} not found")


@app.delete("/persons/{id}", response_description="Delete a person")
async def delete_person(id: str):
    delete_result = await person_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"person {id} not found")
