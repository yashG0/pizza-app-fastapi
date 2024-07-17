import os
from motor.motor_asyncio import AsyncIOMotorClient

database_url = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(database_url)
db_name = client.get_database("pizza_app")

userColl = db_name.get_collection("users")
orderColl = db_name.get_collection("orders")
