from fastapi import APIRouter, HTTPException, Response, Request, Depends
from src.models.user import User, UserOut, UserIn
from src.utils.password import verifyPassword, getHashPassword
from src.configs.db import userColl
from src.utils.jwt_fun import verifyToken, createAccessToken

authRoute = APIRouter()


@authRoute.post("/signup", response_model=UserOut)
async def createUser(form: User, res: Response):
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
        res.set_cookie(key="access_token", value=token, httponly=True, secure=True)
        return UserOut(email=newUser["email"])

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"failed to save new user {e}")


@authRoute.post("/login", response_model=UserOut)
async def verifyUser(form: UserIn, res: Response):
    userExist = await userColl.find_one({"email": form.email})

    # check if the user exist or not
    if not userExist:
        raise HTTPException(status_code=401, detail="User doesn't exist, please sign up first")

    # Verify the password
    if not verifyPassword(form.password, userExist["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Generate a JWT token
    token = createAccessToken({"email": userExist["email"]})

    # Set the token in the response cookie
    res.set_cookie(key="access_token", value=token, httponly=True, secure=True, samesite="Strict")

    return UserOut(email=userExist["email"])


async def getCurrentUser(req: Request) -> UserOut:
    token = req.cookies.get("access_token")

    # checking the token exist ->
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        # Verify the token ->
        payload = await verifyToken(token)
        email = payload.get("email")

        if not email:
            raise HTTPException(status_code=401, detail="Token does not contain email")

        # Retrieve the user from the database
        user = await userColl.find_one({"email": email})

        if not user:
            raise HTTPException(status_code=404, detail="User could not be found")

        return UserOut(email=user["email"])

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Failed to get current user {e}")


@authRoute.get("/user", response_model=UserOut)
async def getUser(current_user: UserOut = Depends(getCurrentUser)):
    return current_user
