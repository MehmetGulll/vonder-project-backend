from fastapi import FastAPI, HTTPException
from .db import get_product_from_db, save_product_to_db
from .vendor_apis import vendor1, vendor2, vendor3
from .kafka import send_to_kafka

app = FastAPI()

@app.get("/product/{product_id}")
async def get_product(product_id: str):
    product = get_product_from_db(product_id)
    if product:
        return product
    
    product_data = await fetch_product_data(product_id)
    if not product_data:
        raise HTTPException(status_code=404, detail="Products not found")
    
    send_to_kafka(product_data)
    return product_data

async def fetch_product_data(product_id: str):
    data=[]
    data.append(await vendor1.get_product(product_id))
    data.append(await vendor2.get_product(product_id))
    data.append(await vendor3.get_product(product_id))
    return unify_data(data)