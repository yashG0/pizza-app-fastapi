import os
from src.models.jwt_token import Token, TokenData
import jwt

KEY = "QifsNW9n6w26mFmeAbEk5yGV3AtVVsQVNGBQa/YitgY"
ALGORITHM = "HS256"


def createAccessToken(data: dict) -> str:
    encoded_jwt = jwt.encode(data, key=KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verifyToken(token: str) -> dict:
    decodedData = jwt.decode(token=token, key=KEY, algorithms=[ALGORITHM])
    return decodedData
