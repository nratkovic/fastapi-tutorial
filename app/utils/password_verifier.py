import re

from passlib.context import CryptContext

# set default hashing algorithm to bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def validate_password(password: str, invalid_password_exception):

    if not re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{8,}", password):
        raise invalid_password_exception

    return password
