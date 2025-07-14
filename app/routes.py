from flask import Blueprint, request, jsonify, render_template, redirect
from bson.objectid import ObjectId
from app.database import mongo
from app.models import Item, User
from datetime import datetime
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

api_bp = Blueprint("api", __name__)

# Initialize JWT in your app factory (in __init__.py)
# from flask_jwt_extended import JWTManager
# jwt = JWTManager(app)

@api_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if User.find_by_username(username):
        return jsonify({"error": "User already exists"}), 409
    User.create_user(username, password)
    return jsonify({"message": "Registration successful"}), 201

@api_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.find_by_username(username)
    if not user or not User.verify_password(user, password):
        return jsonify({"error": "Invalid credentials"}), 401
    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200

# Protect todo routes:
@api_bp.route("/api/todo_entries", methods=["POST"])
@jwt_required()
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
@jwt_required()
def get_items():
    items = mongo.db.todo_entries.find()
    return jsonify([Item.to_dict(item) for item in items])

@api_bp.route("/api/todo_entries/<string:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
    data = request.get_json()
    update_data = {"$set": {"name": data.get("name"), "description":data.get("description")}}
    result = mongo.db.todo_entries.update_one({"_id": ObjectId(item_id)}, update_data)
    if result.matched_count:
        updated_item = mongo.db.todo_entries.find_one({"_id": ObjectId(item_id)}) 
        return jsonify(Item.to_dict(updated_item))
    return jsonify({"error": "Item not found"}), 404

@api_bp.route("/api/todo_entries/<string:item_id>", methods = ['DELETE'])
@jwt_required()
def delete_item(item_id):
    result = mongo.db.todo_entries.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return jsonify({"message": "Item delete is successful"})
    return jsonify({"error": "Item wasnt found"}), 404