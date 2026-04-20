from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, func

Base = declarative_base()


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False)
    description = Column(String(255), nullable=True)
    location = Column(String(64), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    unit_price = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    @property
    def total_value(self) -> float:
        return round(self.quantity * self.unit_price, 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "location": self.location,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_value": self.total_value,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
        }
