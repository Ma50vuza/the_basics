from app.database import mongo
from datetime import datetime

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