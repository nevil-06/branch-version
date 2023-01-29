import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext


ACCESS_TOKEN_EXPIRE_MINUTES = 10  # 10 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
ALGORITHM = "HS256"
JWT_SECRET_KEY =    "c6824c5d1d2c94b01954148c8f6ed87ef1fcc6d7844eca06ea8bc1a875dd33c7"
JWT_REFRESH_SECRET_KEY = "e5d7cb576112cb99dffd8938be0b8d0e13a9f3a7ab5ca1566f9299df445d2e57"    # should be kept secret



def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str: 
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt



def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def decode_access_token(access_token: str) -> dict:
    try:
        decoded_token = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_token["exp"] >= datetime.timestamp(datetime.now()):
            return decoded_token
        else:
            return {"type": "Error", "message": "Token is expired"}
    except JWTError:
        return {"type": "Error", "message": "Token is invalid"}
