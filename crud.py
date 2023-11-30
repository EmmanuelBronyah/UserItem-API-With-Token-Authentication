import os
import uuid
import schema
import models
import token_schema
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

secret_key = os.environ.get('SECRET_KEY')

SECRET_KEY = secret_key
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_user(db: Session, user: schema.UserCreate):
    password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    hashed_password = password_context.hash(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: uuid.UUID):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def get_user_by_name(db: Session, name: str):
    user = db.query(models.User).filter(models.User.name == name).first()
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


def create_item(db: Session, item: schema.ItemCreate, user_id: uuid.UUID):
    item = models.Item(**item.model_dump(exclude_unset=True), owner_id=user_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, item_id: uuid.UUID):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return item


def get_items(db: Session, skip: int = 0, limit: int = 100):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items


# USER AUTHENTICATION

def verify_password(plain_text_password, hashed_password):
    return pwd_context.verify(plain_text_password, hashed_password)


def authenticate_user(db: Session, name: str, password: str):
    user = get_user_by_name(db, name)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(username_data: dict, expiry_time: timedelta or None = None):
    data_to_encode = username_data.copy()
    if expiry_time:
        time_to_expire = datetime.utcnow() + expiry_time
    else:
        time_to_expire = datetime.utcnow() + timedelta(minutes=15)

    data_to_encode.update({'exp': time_to_expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='Could not validate credentials.',
                                         headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credential_exception

        token_data = token_schema.TokenData(username=username)
    except JWTError:
        raise credential_exception

    db_user = get_user_by_name(db, token_data.username)
    if db_user is None:
        raise credential_exception

    return db_user


async def get_current_active_user(current_user: schema.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')

    return current_user
