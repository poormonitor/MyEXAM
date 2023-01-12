from datetime import timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import get_secret_key

SECRET_KEY = get_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/token")
credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(
    uid: str, expires_delta: timedelta = timedelta(minutes=15), **extra_data
) -> str:
    from datetime import datetime

    to_encode = extra_data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"uid": uid})
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        uid: str = payload.get("uid")
        if not uid:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return uid


async def admin_required(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        uid: str = payload.get("uid")
        if not uid:
            raise credentials_exception
        admin = payload.get("admin", False)
    except JWTError:
        raise credentials_exception
    if not admin:
        raise HTTPException(status_code=401, detail="Admin required.")
    return True


def hash_passwd(passwd: str) -> str:
    return pwd_context.hash(passwd)


def verify_passwd(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)