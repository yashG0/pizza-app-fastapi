from fastapi import APIRouter, Depends, Request, HTTPException
from src.routes.auth import getCurrentUser
from src.models.user import UserOut
from src.models.order import Choice, OrderOut
from src.configs.db import orderColl

orderRoute = APIRouter()


@orderRoute.get("/get")
async def displayAll(user: UserOut = Depends(getCurrentUser)) -> dict:
    try:
        userEmail = user.email
        orders = []

        async for order in orderColl.find({"user_email": userEmail}):
            order["_id"] = str(order["_id"])
            orders.append(order)

        return {"orders": orders}

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Failed to fetch order to user {e}")


@orderRoute.post("/create", response_model=OrderOut)
async def createOrder(order: Choice, user: UserOut = Depends(getCurrentUser)):
    try:
        userEmail = user.email

        if not userEmail:
            raise HTTPException(status_code=404, detail="Failed to get user email")

        orderData = order.model_dump()
        orderData["user_email"] = userEmail

        orderInserted = await orderColl.insert_one(orderData)

        if not orderInserted:
            raise HTTPException(status_code=401, detail="Failed to insert order in database!")

        return {"msg": "Order created successfully", "user_email": userEmail}

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Failed to create new order {e}")
