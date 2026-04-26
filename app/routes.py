from flask import Blueprint, request, jsonify, render_template
from app.database import get_session
from app.service import InventoryService

inventory_bp = Blueprint("inventory", __name__, template_folder='templates', static_folder='static')


def _json_error(message, status=400):
    return jsonify({"error": message}), status


# Web UI route
@inventory_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@inventory_bp.route("/items", methods=["GET"])
def list_items():
    query = request.args.get("q")
    with get_session() as session:
        service = InventoryService(session)
        items = service.list_items(query)
        return jsonify({"items": items})


@inventory_bp.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    with get_session() as session:
        service = InventoryService(session)
        try:
            item = service.get_item(item_id)
        except ValueError as exc:
            return _json_error(str(exc), 404)
        return jsonify(item.to_dict())


@inventory_bp.route("/items", methods=["POST"])
def create_item():
    payload = request.get_json(silent=True) or {}
    with get_session() as session:
        service = InventoryService(session)
        try:
            item = service.create_item(payload)
        except ValueError as exc:
            return _json_error(str(exc), 422)
        return jsonify(item.to_dict()), 201


@inventory_bp.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    payload = request.get_json(silent=True) or {}
    with get_session() as session:
        service = InventoryService(session)
        try:
            item = service.update_item(item_id, payload)
        except ValueError as exc:
            return _json_error(str(exc), 422 if "not found" not in str(exc).lower() else 404)
        return jsonify(item.to_dict())


@inventory_bp.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    with get_session() as session:
        service = InventoryService(session)
        try:
            service.delete_item(item_id)
        except ValueError as exc:
            return _json_error(str(exc), 404)
        return jsonify({"message": "Item deleted"}), 200


@inventory_bp.route("/items/<int:item_id>/stock", methods=["POST"])
def adjust_stock(item_id):
    payload = request.get_json(silent=True) or {}
    amount = payload.get("amount")
    with get_session() as session:
        service = InventoryService(session)
        try:
            amount_value = int(amount)
            item = service.adjust_stock(item_id, amount_value)
        except (TypeError, ValueError) as exc:
            return _json_error(str(exc), 422)
        return jsonify(item.to_dict())


@inventory_bp.route("/summary", methods=["GET"])
def summary():
    with get_session() as session:
        service = InventoryService(session)
        items = service.list_items()
        total_items = len(items)
        stock_value = sum(item["total_value"] for item in items)
        return jsonify({"total_items": total_items, "total_stock_value": round(stock_value, 2)})
