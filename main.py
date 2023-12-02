import uuid
import crud
import schema
import models
import token_schema
from functools import partial
from datetime import timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# modifies the get_current_user function where the db parameter is fixed
# on the result of the get_db function.
partial_func_get_current_user = partial(crud.get_current_user, db=Depends(get_db))


@app.get('/')
async def home():
    content = (
        "To create a user: /create-user/ \n"
        "To get a user: /get-user/:userId/ \n"
        "To get users: /get-users/ \n"
        "To create an item: /create-item/ \n"
        "To get an item: /get-item/:itemId/ \n"
        "To get items: /get-items/ \n"
        "To get access token: /token/"
    )
    return PlainTextResponse(content=content, media_type="text/plain")


@app.post('/create-user/', response_model=schema.User)
async def create_user(
        user: schema.UserCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(partial_func_get_current_user)
):
    if current_user:
        db_user = crud.create_user(db, user)
        return db_user


@app.get('/get-user/{user_id}/', response_model=schema.User)
async def get_user(
        user_id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(partial_func_get_current_user)

):
    if current_user:
        user = crud.get_user(db, user_id)
        if not user:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
        return user


@app.get('/get-users/', response_model=list[schema.User])
async def get_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(partial_func_get_current_user)
):
    if current_user:
        users = crud.get_users(db, skip, limit)
        if not users:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Users not found.')
        return users


@app.post('/create-item/', response_model=schema.Item)
async def create_item(item: schema.ItemCreate,
                      user_id: uuid.UUID,
                      db: Session = Depends(get_db),
                      current_user: models.User = Depends(partial_func_get_current_user)
                      ):
    if current_user:
        return crud.create_item(db, item, user_id)


@app.get('/get-item/{item_id}', response_model=schema.Item)
async def get_item(
        item_id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(partial_func_get_current_user)
):
    if current_user:
        item = crud.get_item(db, item_id)
        if not item:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found.')
        return item


@app.get('/get-items/', response_model=list[schema.Item])
async def get_items(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(partial_func_get_current_user)
):
    if current_user:
        items = crud.get_items(db, skip, limit)
        if not items:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Items not found.')
        return items


@app.post('/token/', response_model=token_schema.Token)
async def login_for_access_token(db: Session = Depends(get_db),
                                 form_data: OAuth2PasswordRequestForm = Depends()
                                 ):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password',
                            headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(username_data={'sub': user.name},
                                            expiry_time=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
