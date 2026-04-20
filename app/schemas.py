from typing import Tuple, Dict, Any


def validate_item_payload(payload: Dict[str, Any], partial: bool = False) -> Tuple[bool, str]:
    if not isinstance(payload, dict):
        return False, "Payload must be a JSON object"

    required_fields = ["name", "category", "location", "quantity", "unit_price"]
    if not partial:
        missing = [field for field in required_fields if field not in payload]
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"

    if "name" in payload and not payload["name"]:
        return False, "Item name cannot be empty"
    if "category" in payload and not payload["category"]:
        return False, "Item category cannot be empty"
    if "location" in payload and not payload["location"]:
        return False, "Item location cannot be empty"

    if "quantity" in payload:
        try:
            quantity = int(payload["quantity"])
        except (TypeError, ValueError):
            return False, "Quantity must be an integer"
        if quantity < 0:
            return False, "Quantity cannot be negative"

    if "unit_price" in payload:
        try:
            unit_price = float(payload["unit_price"])
        except (TypeError, ValueError):
            return False, "Unit price must be a number"
        if unit_price < 0:
            return False, "Unit price cannot be negative"

    return True, ""


def normalize_item_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    if "name" in payload:
        normalized["name"] = str(payload["name"]).strip()
    if "category" in payload:
        normalized["category"] = str(payload["category"]).strip()
    if "description" in payload:
        normalized["description"] = str(payload["description"]).strip()
    if "location" in payload:
        normalized["location"] = str(payload["location"]).strip()
    if "quantity" in payload:
        normalized["quantity"] = int(payload["quantity"])
    if "unit_price" in payload:
        normalized["unit_price"] = float(payload["unit_price"])
    return normalized
