import pytest
from app.adapters.vendor_adapter import map_vendor_data_to_standard


def test_map_vendor_data_to_standard():
    vendor_data = {"ProductName": "Test Product", "ProductPrice": 50.0}
    field_mapping = {"ProductName": "name", "ProductPrice": "price"}

    standardized_data = map_vendor_data_to_standard(vendor_data, field_mapping)
    assert standardized_data["name"] == "Test Product"
    assert standardized_data["price"] == 50.0
