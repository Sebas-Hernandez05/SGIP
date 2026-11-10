"""HTTP registration entry point; callers cannot choose role or account state."""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.repositories.citizens import CitizenRepository, DatabaseUnavailable, DuplicateEmail
from app.schemas.citizens import CitizenPublic, CitizenRegistration
from app.services.citizens import CitizenService

router = APIRouter(prefix="/api/v1", tags=["ciudadanos"])


def get_citizen_repository() -> CitizenRepository:
    return CitizenRepository()


@router.post("/ciudadanos", status_code=status.HTTP_201_CREATED, response_model=CitizenPublic,
             responses={409: {"description": "Correo duplicado"}, 503: {"description": "Persistencia no disponible"}})
def register_citizen(payload: CitizenRegistration, response: Response,
                     repository: Annotated[CitizenRepository, Depends(get_citizen_repository)]):
    response.headers["Cache-Control"] = "no-store"
    try:
        return CitizenService(repository).register(payload.nombre, str(payload.correo), payload.contrasena)
    except DuplicateEmail:
        raise HTTPException(status_code=409, detail="El correo ya está registrado.") from None
    except DatabaseUnavailable:
        raise HTTPException(status_code=503, detail="El servicio no está disponible. Intenta más tarde.") from None
