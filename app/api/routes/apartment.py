from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.apartment import ApartmentCreate, ApartmentResponse, ApartmentUpdate
from app.services.apartment_service import ApartmentService


router = APIRouter(prefix="/api/apartments", tags=["Apartments"])
service = ApartmentService()


@router.get("", response_model=list[ApartmentResponse])
def get_apartments(
    search: str | None = Query(default=None, max_length=100),
    db: Session = Depends(get_db),
):
    return service.get_all(db, search)


@router.get("/{apartment_id}", response_model=ApartmentResponse)
def get_apartment(
    apartment_id: int,
    db: Session = Depends(get_db),
):
    return service.get_by_id(db, apartment_id)


@router.post(
    "",
    response_model=ApartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_apartment(
    data: ApartmentCreate,
    db: Session = Depends(get_db),
):
    return service.create(db, data)


@router.put("/{apartment_id}", response_model=ApartmentResponse)
def update_apartment(
    apartment_id: int,
    data: ApartmentUpdate,
    db: Session = Depends(get_db),
):
    return service.update(db, apartment_id, data)


@router.delete("/{apartment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_apartment(
    apartment_id: int,
    db: Session = Depends(get_db),
):
    service.delete(db, apartment_id)
    return None
