from app.database import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User:
    @staticmethod
    def create_user(username, email, password):
        hashed = generate_password_hash(password)
        user = {"username": username, "email": email, "password": hashed}
        mongo.db.users.insert_one(user)
        return user

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user["password"], password)

class Item:
    @staticmethod
    def to_dict(item):
        #time = datetime().isoformat()
        return {
            "id": str(item["_id"]),
            "name": item["name"],
            #"description": item.get("description", ""),
            #"time": time
        }