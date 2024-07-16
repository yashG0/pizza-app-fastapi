from passlib.context import CryptContext

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verifyPassword(password: str, hashPassword: str) -> bool:
    return passwordContext.verify(password, hashPassword)


def getHashPassword(password: str) -> str:
    return passwordContext.hash(password)
