from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-jwt-key-change-this-in-production-12345")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Security - Fixed bcrypt implementation
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secure user store with proper bcrypt hashes
USERS_DB = {
    "demo": "$2b$12$xyZc9jWa0iMifjL9BrZ31.ZpHfc.ysr3KP6LpAC3DX8nbfmdc63he",  # demo
    "admin": "$2b$12$.QcUVLxReQlfviq0X3hCOOLjCfFubuaf6AIUh1cQXOzQqzDCNf8k2",  # demo
    "reviewer": "$2b$12$UNstFuAza1Epla3EvC0HhuCB4vqn13tEp38EfDbC4ffPZDpzIm0lC"  # demo
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using bcrypt - secure implementation"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def hash_password(password: str) -> str:
    """Hash password using bcrypt for new users"""
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    """Authenticate user with secure password verification"""
    if username not in USERS_DB:
        return False
    if not verify_password(password, USERS_DB[username]):
        return False
    return username

def create_access_token(data: dict):
    """Create JWT token with proper timezone-aware expiration"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token with proper expiration checking"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Check token expiration properly
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(status_code=401, detail="Token missing expiration")
        
        if datetime.now(timezone.utc).timestamp() > exp:
            raise HTTPException(status_code=401, detail="Token expired")
            
        return username
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def get_current_user(token: str = Depends(verify_token)):
    return token
