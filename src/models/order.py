from pydantic import BaseModel, Field
from enum import Enum
from bson import ObjectId


class Choice(BaseModel):
    quantity: int = 0
    order_status: Enum("pending", "deliver", "in_transit") = "pending"
    pizza_size: Enum("small", "medium", "large", "extra_large") = "small"
    user_id: ObjectId
