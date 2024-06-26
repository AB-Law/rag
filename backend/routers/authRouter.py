from config.auth import *
from schema.token import Token
from models.user import User
from schema.userSchema import UserOut
from fastapi import Depends, HTTPException, status, Request
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from database.auth import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    try:
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    except Exception as e:
        raise e  # Re-raise the exception to maintain original behavior



# Modify login_for_access_token function to include error logging
from fastapi import HTTPException, status

@router.post("/token", tags =["Auth"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    db: Session = Depends(get_db)
) -> Token:
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    
    except Exception as e:
        raise e


@router.get("/users/me/", response_model=UserOut, tags =["UserDB"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/users/me/items/", tags =["UserDB"])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.post("/getAllUsers", response_model=list[UserOut], tags =["UserDB"])
async def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)
    

@router.post("/register", response_model=UserOut, tags =["Auth"])
async def register_user(
    username: str,
    full_name: str,
    email: str,
    password: str,
    request: Request,
    db: Session = Depends(get_db),
    
):
    # Check if username already exists
    existing_user = get_user(db, username=username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Create the user
    hashed_password = pwd_context.hash(password)
    db_user = User(
        username=username,
        full_name=full_name,
        email=email,
        password=hashed_password,
        disabled=False  # You may adjust this as needed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user