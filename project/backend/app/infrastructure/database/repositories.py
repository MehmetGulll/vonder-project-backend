from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.base import Base
from sqlalchemy import Column, String, Float, JSON

# ORM Model
class ProductORM(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    photos = Column(JSON)


# Repository Sınıfı
class SQLAlchemyProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_products(self, limit: int, offset: int):
        query = select(ProductORM).limit(limit).offset(offset)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def save_product(self, product: dict):
        orm_product = ProductORM(**product)
        self.db.add(orm_product)
        await self.db.commit()
