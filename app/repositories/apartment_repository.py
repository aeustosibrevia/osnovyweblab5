from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models import Apartment
from app.schemas.apartment import ApartmentCreate, ApartmentUpdate


class ApartmentRepository:
    def get_all(self, db: Session, search: str | None = None) -> list[Apartment]:
        statement = select(Apartment).order_by(Apartment.id.desc())

        if search and search.strip():
            term = f"%{search.strip()}%"
            statement = statement.where(
                or_(
                    Apartment.district.ilike(term),
                    Apartment.address.ilike(term),
                    Apartment.owner_name.ilike(term),
                )
            )

        return list(db.scalars(statement).all())

    def get_by_id(self, db: Session, apartment_id: int) -> Apartment | None:
        return db.get(Apartment, apartment_id)

    def create(self, db: Session, data: ApartmentCreate) -> Apartment:
        apartment = Apartment(**data.model_dump())
        db.add(apartment)
        db.commit()
        db.refresh(apartment)
        return apartment

    def update(
        self,
        db: Session,
        apartment: Apartment,
        data: ApartmentUpdate,
    ) -> Apartment:
        for field, value in data.model_dump().items():
            setattr(apartment, field, value)

        db.commit()
        db.refresh(apartment)
        return apartment

    def delete(self, db: Session, apartment: Apartment) -> None:
        db.delete(apartment)
        db.commit()
