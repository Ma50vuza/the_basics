from flask import Flask
from pymongo import MongoClient
from app import create_app
import os




app = create_app()

#MongoDB Atlas conn
#MONGO_URI = os.environ.get("MONGO_URI")
#client = MongoClient(MONGO_URI)
#db = client["todo_lists"]
#collection = ["todo_entries"]

#Saving to MDB
#todo_data = {
#   "user": user,
#    "entry":usr_entry,
#    "user_id":user_id,
#}
#collection.insert_one(todo_data)
#print(f"{user}'s data has been added to the DB")

if __name__ == "__main__":
    app.run(debug=True)