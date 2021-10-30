import hashlib
import jwt


def hash_password(password: str) -> str:
    return hashlib.sha1(password.encode('utf-8')).hexdigest()


def create_token(username: str, secret_key: str) -> str:
    return jwt.encode(
        {"name": username},
        secret_key,
        algorithm="HS256"
    )

