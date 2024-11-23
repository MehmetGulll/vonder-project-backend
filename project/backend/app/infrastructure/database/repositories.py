from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.base import Base
from sqlalchemy import Column, String, Float, JSON


class ProductORM(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    photos = Column(JSON)



class SQLAlchemyProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_products(self, limit: int, offset: int):
        query = select(ProductORM).limit(limit).offset(offset)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def save_product(self, product: dict):
        try:
            orm_product = ProductORM(**product)
            print(f"[DEBUG] Saving product: {orm_product}")
            self.db.add(orm_product)
            await self.db.commit()
            print(f"[DEBUG] Product saved successfully: {orm_product.id}")
        except Exception as e:
            print(f"[ERROR] Failed to save product: {e}")
            raise

