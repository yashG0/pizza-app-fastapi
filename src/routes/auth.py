from fastapi import APIRouter

authRoute = APIRouter()


@authRoute.get("/")
async def root():
    return {"msg":"welcome to auth page"}
