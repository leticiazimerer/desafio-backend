from bson import ObjectId
from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class PersonModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    address: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Leticia",
                "last_name": "Zimerer",
                "email": "leticiazimerer@gmail.com",
                "address": "Avenida Paulista, 537",
            }
        },
    )


class UpdatePersonModel(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Leticia",
                "last_name": "Zimerer",
                "email": "leticiazimerer@gmail.com",
                "address": "Avenida Paulista, 537",
            }
        },
    )


class PersonCollection(BaseModel):
    persons: List[PersonModel]

