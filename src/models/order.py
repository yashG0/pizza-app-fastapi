from pydantic import BaseModel, Field
from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    deliver = "deliver"
    in_transit = "in_transit"


class PizzaSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"
    extra_large = "extra_large"


class Choice(BaseModel):
    quantity: int = Field(..., description="Quantity of pizzas", gt=0)
    order_status: OrderStatus = Field(OrderStatus.pending, description="Status of the order")
    pizza_size: PizzaSize = Field(PizzaSize.small, description="Size of the pizza")
    user_email: str | None = Field(None, description="Email of the user")


class OrderOut(BaseModel):
    user_email: str
