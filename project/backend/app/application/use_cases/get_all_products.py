from typing import Dict, Any
from app.infrastructure.database.database_adapter import async_get_all_products


async def get_all_products(limit: int, offset: int) -> Dict[str, Any]:
    try:

        products = await async_get_all_products(limit, offset)
        if not products:
            return {"message": "No products found"}


        grouped_products = {}
        for product in products:
            vendor_name = product["id"].split("-")[0]
            grouped_products.setdefault(vendor_name, []).append(product)

        return {"data": grouped_products}

    except Exception as e:

        return {"error": f"Error fetching products: {str(e)}"}
