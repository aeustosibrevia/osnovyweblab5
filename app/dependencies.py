from app.services.apartment_service import ApartmentService


def get_apartment_service() -> ApartmentService:
    return ApartmentService()
