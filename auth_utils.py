import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha1(password.encode('utf-8')).hexdigest()
