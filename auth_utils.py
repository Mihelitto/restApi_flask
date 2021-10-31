import hashlib
import jwt
from jwt.exceptions import InvalidTokenError
from db import User, session


def hash_password(password: str) -> str:
    return hashlib.sha1(password.encode('utf-8')).hexdigest()


def create_token(username: str, secret_key: str) -> str:
    return jwt.encode(
        {"name": username},
        secret_key,
        algorithm="HS256"
    )


def decode_token(token: str, secret_key: str) -> dict:
    return jwt.decode(token, secret_key, algorithms="HS256")


def check_token(auth_credentials: str, secret_key: str) -> None:
    if not auth_credentials:
        raise ValueError
    scheme, token = auth_credentials.split()
    if scheme != 'bearer':
        raise ValueError

    decoded_token = decode_token(token, secret_key)
    user_exists = (
        session
        .query(
            session
            .query(User)
            .filter(User.name == decoded_token['name'])
            .exists()
        )
        .scalar()
    )
    if not user_exists:
        raise InvalidTokenError
