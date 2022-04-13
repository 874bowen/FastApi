from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET KEY
# openssl rand -hex 32
# from secrets import token_bytes
# from base64 import b64encode
#
# print(b64encode(token_bytes(32)).decode())
SECRET_KEY = "Svj/QuHTMLI42ywAHAS9MmX63mAFP8+0NUB0B5bmKcM="

# Algorithm
ALGORITHM = "HS256"
# Expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt