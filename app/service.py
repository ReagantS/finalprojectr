from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from app.models import InventoryItem
from app.schemas import validate_item_payload, normalize_item_payload


class InventoryService:
    def __init__(self, session):
        self.session = session

    def calculate_total_value(self, quantity: int, unit_price: float) -> float:
        return round(quantity * unit_price, 2)

    def list_items(self, query: str = None):
        stmt = select(InventoryItem)
        if query:
            like_query = f"%{query}%"
            stmt = stmt.where(
                InventoryItem.name.ilike(like_query)
                | InventoryItem.category.ilike(like_query)
            )
        return [item.to_dict() for item in self.session.execute(stmt).scalars().all()]

    def get_item(self, item_id: int):
        stmt = select(InventoryItem).where(InventoryItem.id == item_id)
        item = self.session.execute(stmt).scalar_one_or_none()
        if not item:
            raise ValueError("Item not found")
        return item

    def create_item(self, payload: dict):
        valid, message = validate_item_payload(payload)
        if not valid:
            raise ValueError(message)

        data = normalize_item_payload(payload)
        item = InventoryItem(**data)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update_item(self, item_id: int, payload: dict):
        valid, message = validate_item_payload(payload, partial=True)
        if not valid:
            raise ValueError(message)

        item = self.get_item(item_id)
        data = normalize_item_payload(payload)
        for key, value in data.items():
            setattr(item, key, value)
        self.session.commit()
        self.session.refresh(item)
        return item

    def adjust_stock(self, item_id: int, amount: int):
        item = self.get_item(item_id)
        if not isinstance(amount, int):
            raise ValueError("Stock adjustment amount must be an integer")
        new_quantity = item.quantity + amount
        if new_quantity < 0:
            raise ValueError("Stock adjustment would create negative quantity")
        item.quantity = new_quantity
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete_item(self, item_id: int):
        item = self.get_item(item_id)
        self.session.delete(item)
        self.session.commit()
        return item
