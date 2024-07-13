from fastapi import FastAPI
from src.routes import auth, order
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# different api routes ->
app.include_router(auth.authRoute, prefix="/api/auth", tags=["our auth api"])
app.include_router(order.orderRoute, prefix="/api/order", tags=["our orders api"])
