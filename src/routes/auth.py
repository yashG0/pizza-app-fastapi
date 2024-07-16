from fastapi import APIRouter, HTTPException
from src.models.user import User, UserOut, UserIn
from src.utils.password import verifyPassword, getHashPassword
from src.configs.db import userColl, orderColl
from src.utils.jwt_fun import verifyToken,createAccessToken

authRoute = APIRouter()


@authRoute.post("/signup", response_model=UserOut)
async def createUser(form: User):
    try:
        newUser = form.model_dump()

        # check the user if exist
        existingUser = await userColl.find_one({"email": newUser["email"]})

        # raise the http error if user already exist in database
        if existingUser:
            raise HTTPException(status_code=400, detail="Email already registered")

        # hash the user password
        newUser["password"] = getHashPassword(newUser["password"])

        # finally, save the user into database
        await userColl.insert_one(newUser)
        token = createAccessToken({"email": newUser["email"]})
        # print(token)
        return UserOut(email=newUser["email"])

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"failed to save new user {e}")


@authRoute.post("/login", response_model=UserOut)
async def verifyUser(form:UserIn):
    pass
