from flask import Blueprint, request, jsonify, render_template, redirect
from bson.objectid import ObjectId
from app.database import mongo
from app.models import Item
from datetime import datetime
api_bp = Blueprint("api", __name__)


@api_bp.route("/api/todo_entries", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Invalid input, 'name' is required and JSON must be sent"}), 400
    name = data["name"]
    timestamp = datetime.now().isoformat()
    item = {"name": name, "time": timestamp}
    result = mongo.db.todo_entries.insert_one(item)
    objId = str(result.inserted_id)
    return jsonify({"id": objId, "name": name, "time": timestamp}), 201

@api_bp.route("/api/todo_entries", methods=["GET"])
def get_items():
    items = mongo.db.todo_entries.find()
    return jsonify([Item.to_dict(item) for item in items])

@api_bp.route("/api/todo_entries/<string:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    update_data = {"$set": {"name": data.get("name"), "description":data.get("description")}}
    result = mongo.db.todo_entries.update_one({"_id": ObjectId(item_id)}, update_data)
    if result.matched_count:
        updated_item = mongo.db.todo_entries.find_one({"_id": ObjectId(item_id)}) 
        return jsonify(Item.to_dict(updated_item))
    return jsonify({"error": "Item not found"}), 404

@api_bp.route("/api/todo_entries/<string:item_id>", methods = ['DELETE'])
def delete_item(item_id):
    result = mongo.db.todo_entries.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return jsonify({"message": "Item delete is successful"})
    return jsonify({"error": "Item wasnt found"}), 404