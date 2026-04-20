import json


def test_get_empty_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.get_json()["items"] == []


def test_create_item_endpoint(client):
    payload = {
        "name": "USB Drive",
        "category": "Electronics",
        "description": "16GB storage",
        "location": "Shelf 1",
        "quantity": 8,
        "unit_price": 7.5,
    }
    response = client.post("/items", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "USB Drive"
    assert data["total_value"] == 60.0


def test_get_item_endpoint(client):
    payload = {
        "name": "Mouse",
        "category": "Electronics",
        "location": "Shelf 2",
        "quantity": 5,
        "unit_price": 12.0,
    }
    create_response = client.post("/items", data=json.dumps(payload), content_type="application/json")
    item_id = create_response.get_json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Mouse"


def test_update_item_endpoint(client):
    payload = {
        "name": "Keyboard",
        "category": "Electronics",
        "location": "Shelf 3",
        "quantity": 3,
        "unit_price": 20.0,
    }
    create_response = client.post("/items", data=json.dumps(payload), content_type="application/json")
    item_id = create_response.get_json()["id"]

    update_payload = {"quantity": 10, "unit_price": 18.0}
    response = client.put(f"/items/{item_id}", data=json.dumps(update_payload), content_type="application/json")
    assert response.status_code == 200
    assert response.get_json()["quantity"] == 10
    assert response.get_json()["unit_price"] == 18.0


def test_adjust_stock_endpoint(client):
    payload = {
        "name": "Notebook",
        "category": "Stationery",
        "location": "Shelf 4",
        "quantity": 15,
        "unit_price": 2.5,
    }
    create_response = client.post("/items", data=json.dumps(payload), content_type="application/json")
    item_id = create_response.get_json()["id"]

    response = client.post(
        f"/items/{item_id}/stock",
        data=json.dumps({"amount": -5}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.get_json()["quantity"] == 10


def test_delete_item_endpoint(client):
    payload = {
        "name": "Label Printer",
        "category": "Equipment",
        "location": "Shelf 5",
        "quantity": 2,
        "unit_price": 55.0,
    }
    create_response = client.post("/items", data=json.dumps(payload), content_type="application/json")
    item_id = create_response.get_json()["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Item deleted"

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404
