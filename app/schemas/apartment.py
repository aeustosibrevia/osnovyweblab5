import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ApartmentBase(BaseModel):
    district: str = Field(min_length=2, max_length=100)
    address: str = Field(min_length=5, max_length=200)
    floor: int = Field(ge=1, le=100)
    area: float = Field(gt=0, le=10000)
    rooms: int = Field(ge=1, le=20)
    owner_name: str = Field(min_length=2, max_length=100)
    owner_phone: str = Field(min_length=7, max_length=25)
    price: float = Field(gt=0, le=1_000_000_000)

    @field_validator("district", "address", "owner_name", "owner_phone")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Поле не може бути порожнім")
        return value

    @field_validator("owner_phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.fullmatch(r"[+()\-\d\s]+", value):
            raise ValueError("Некоректний номер телефону")
        return value


class ApartmentCreate(ApartmentBase):
    pass


class ApartmentUpdate(ApartmentBase):
    pass


class ApartmentResponse(ApartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
