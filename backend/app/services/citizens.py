"""Registration business rules; persistence remains in the repository."""
from app.core.security import hash_password
from app.repositories.citizens import CitizenRepository


class CitizenService:
    def __init__(self, repository: CitizenRepository):
        self.repository = repository

    def register(self, nombre: str, correo: str, contrasena: str) -> dict:
        return self.repository.create(nombre, correo, hash_password(contrasena))
