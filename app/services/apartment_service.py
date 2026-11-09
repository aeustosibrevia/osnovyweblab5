from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Apartment
from app.repositories.apartment_repository import ApartmentRepository
from app.schemas.apartment import ApartmentCreate, ApartmentUpdate


class ApartmentService:
    def __init__(self, repository: ApartmentRepository | None = None):
        self.repository = repository or ApartmentRepository()

    def get_all(self, db: Session, search: str | None = None) -> list[Apartment]:
        return self.repository.get_all(db, search)

    def get_by_id(self, db: Session, apartment_id: int) -> Apartment:
        apartment = self.repository.get_by_id(db, apartment_id)
        if apartment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Квартиру не знайдено",
            )
        return apartment

    def create(self, db: Session, data: ApartmentCreate) -> Apartment:
        return self.repository.create(db, data)

    def update(
        self,
        db: Session,
        apartment_id: int,
        data: ApartmentUpdate,
    ) -> Apartment:
        apartment = self.get_by_id(db, apartment_id)
        return self.repository.update(db, apartment, data)

    def delete(self, db: Session, apartment_id: int) -> None:
        apartment = self.get_by_id(db, apartment_id)
        self.repository.delete(db, apartment)
