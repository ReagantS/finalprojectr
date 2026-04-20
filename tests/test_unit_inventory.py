import pytest
from app.database import get_session
from app.service import InventoryService


@pytest.fixture
def service():
    with get_session() as session:
        yield InventoryService(session)


def test_validate_item_payload_rejects_empty_name(service):
    with pytest.raises(ValueError):
        service.create_item({"name": "", "category": "Office", "location": "Warehouse", "quantity": 10, "unit_price": 5.0})


def test_validate_item_payload_rejects_negative_quantity(service):
    with pytest.raises(ValueError):
        service.create_item({"name": "Printer", "category": "Office", "location": "Warehouse", "quantity": -1, "unit_price": 100.0})


def test_validate_item_payload_rejects_negative_price(service):
    with pytest.raises(ValueError):
        service.create_item({"name": "Monitor", "category": "Office", "location": "Warehouse", "quantity": 5, "unit_price": -10.0})


def test_create_item_persists_record(service):
    item = service.create_item({"name": "Desk", "category": "Furniture", "location": "Warehouse A", "quantity": 3, "unit_price": 120.0})
    assert item.id is not None
    assert item.quantity == 3
    assert item.unit_price == 120.0


def test_calculate_total_value(service):
    assert service.calculate_total_value(4, 25.5) == 102.0


def test_update_item_changes_fields(service):
    item = service.create_item({"name": "Chair", "category": "Furniture", "location": "Warehouse B", "quantity": 12, "unit_price": 45.0})
    updated = service.update_item(item.id, {"quantity": 15, "unit_price": 40.0})
    assert updated.quantity == 15
    assert updated.unit_price == 40.0


def test_adjust_stock_increases_quantity(service):
    item = service.create_item({"name": "Paper", "category": "Supply", "location": "Warehouse C", "quantity": 50, "unit_price": 0.5})
    adjusted = service.adjust_stock(item.id, 10)
    assert adjusted.quantity == 60


def test_adjust_stock_decreases_quantity(service):
    item = service.create_item({"name": "Pen", "category": "Supply", "location": "Warehouse C", "quantity": 20, "unit_price": 1.5})
    adjusted = service.adjust_stock(item.id, -5)
    assert adjusted.quantity == 15


def test_adjust_stock_rejects_negative_result(service):
    item = service.create_item({"name": "Stapler", "category": "Supply", "location": "Warehouse D", "quantity": 2, "unit_price": 8.0})
    with pytest.raises(ValueError):
        service.adjust_stock(item.id, -5)


def test_delete_item_removes_record(service):
    item = service.create_item({"name": "Folder", "category": "Supply", "location": "Warehouse D", "quantity": 8, "unit_price": 2.0})
    service.delete_item(item.id)
    with pytest.raises(ValueError):
        service.get_item(item.id)


def test_search_items_matches_name(service):
    service.create_item({"name": "Whiteboard", "category": "Office", "location": "Warehouse E", "quantity": 1, "unit_price": 220.0})
    results = service.list_items("white")
    assert len(results) == 1


def test_list_items_returns_all(service):
    service.create_item({"name": "Marker", "category": "Office", "location": "Warehouse E", "quantity": 10, "unit_price": 1.2})
    service.create_item({"name": "Eraser", "category": "Office", "location": "Warehouse E", "quantity": 4, "unit_price": 0.8})
    assert len(service.list_items()) >= 2


def test_partial_update_preserves_fields(service):
    item = service.create_item({"name": "Clipboard", "category": "Office", "location": "Warehouse F", "quantity": 7, "unit_price": 4.5})
    updated = service.update_item(item.id, {"quantity": 9})
    assert updated.quantity == 9
    assert updated.name == "Clipboard"


def test_update_item_rejects_invalid_quantity(service):
    item = service.create_item({"name": "Calculator", "category": "Office", "location": "Warehouse G", "quantity": 5, "unit_price": 15.0})
    with pytest.raises(ValueError):
        service.update_item(item.id, {"quantity": -3})


def test_create_item_requires_category_and_location(service):
    with pytest.raises(ValueError):
        service.create_item({"name": "Calculator", "quantity": 5, "unit_price": 15.0})
