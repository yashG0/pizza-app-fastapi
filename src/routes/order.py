from fastapi import APIRouter

orderRoute = APIRouter()


@orderRoute.get("/")
async def root():
    return {"msg": "welcome to order page"}
