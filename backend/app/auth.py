from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
import hashlib

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Security
security = HTTPBearer()

# Simple hash function (temporary fix for bcrypt issues)
def simple_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Simple user store
USERS_DB = {
    "demo": simple_hash("demo"),
    "admin": simple_hash("demo"), 
    "reviewer": simple_hash("demo")
}

def verify_password(plain_password, hashed_password):
    return simple_hash(plain_password) == hashed_password

def authenticate_user(username: str, password: str):
    if username not in USERS_DB:
        return False
    if not verify_password(password, USERS_DB[username]):
        return False
    return username

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(verify_token)):
    return token
