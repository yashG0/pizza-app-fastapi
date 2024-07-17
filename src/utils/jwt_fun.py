import os
from src.models.jwt_token import Token, TokenData
import jwt
from fastapi import HTTPException

KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def createAccessToken(data: dict) -> str:
    encoded_jwt = jwt.encode(data, key=KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verifyToken(token: str) -> dict:
    try:
        decoded_data = jwt.decode(token, key=KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error decoding token: {str(e)}")
