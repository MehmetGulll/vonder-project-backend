from app.adapters.vendor_adapter import get_all_vendors_and_product_ids, get_product_from_vendor
from app.infrastructure.database.database_adapter import async_save_product_to_db

async def fetch_and_save_initial_products():
    vendors, product_ids = get_all_vendors_and_product_ids()
    print(f"Vendors: {vendors}, Product IDs: {product_ids}")

    for product_id in product_ids:
        for vendor_name in vendors:
            try:
                print(f"Fetching product {product_id} from vendor {vendor_name}")
                vendor_data = await get_product_from_vendor(vendor_name, product_id)

                if not vendor_data:
                    print(f"No data returned for product {product_id} from vendor {vendor_name}")
                    continue

                vendor_data["id"] = vendor_data.get("id", f"{vendor_name}-{product_id}")
                vendor_data["photos"] = vendor_data.get("photos", ["https://example.com/default-image.jpg"])

                print(f"Fetched vendor data: {vendor_data}")

                await async_save_product_to_db(vendor_data, vendor_name)
            except Exception as e:
                print(f"Error fetching product {product_id} from {vendor_name}: {e}")

