"""Public registration contract shared by web and mobile clients."""
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CitizenRegistration(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, hide_input_in_errors=True)
    nombre: str = Field(min_length=2, max_length=120, pattern=r"^[^\x00]*$")
    correo: EmailStr = Field(max_length=254)
    contrasena: str = Field(min_length=12, max_length=128, repr=False)

    @field_validator("nombre", "correo", mode="before")
    @classmethod
    def normalize(cls, value: object, info):
        if isinstance(value, str):
            normalized = value.strip()
            return normalized.lower() if info.field_name == "correo" else normalized
        return value


class CitizenPublic(BaseModel):
    id: UUID
    nombre: str
    correo: str
    rol: Literal["ciudadano"]
    estado: Literal["activo"]
    fecha_registro: datetime
