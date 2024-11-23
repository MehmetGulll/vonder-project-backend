from fastapi import APIRouter, Depends
from app.application.use_cases import GetAllProductsUseCase
from app.infrastructure.database.repositories import SQLAlchemyProductRepository
from app.infrastructure.database.base import get_db
from app.domain.services import ProductService

router = APIRouter()

@router.get("/products")
async def get_products(limit: int = 10, offset: int = 0, db=Depends(get_db)):
    repository = SQLAlchemyProductRepository(db)
    service = ProductService(repository)
    use_case = GetAllProductsUseCase(service)
    return await use_case.execute(limit, offset)
