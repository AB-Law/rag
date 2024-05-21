from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String, Boolean, create_engine, text
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import User
from schema.userSchema import UserOut
from passlib.context import CryptContext
from fastapi import APIRouter
from sqlalchemy.ext.declarative import declarative_base
from jose import JWTError, jwt
from config.auth import *
from schema.token import *
from models.user import *
from config.database import dbConfig

from urllib.parse import quote_plus

load_dotenv()

# Now instantiate the dbConfig class
dbConfig = dbConfig()

encoded_password = quote_plus(dbConfig.SERVER_PASSWORD.encode('utf-8'))

connection_string = (
    f"postgresql+psycopg2://{dbConfig.SERVER_USERNAME}:{encoded_password}" +
    f"@{dbConfig.SERVER_HOST}:5432/{dbConfig.SERVER_DATABASE}"
)
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()
Base = declarative_base()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, username: str):
    try:
        return db.query(User).filter(User.username == username).first()
    except Exception as e:
        raise e

def get_all_users(db: Session):
    try:
        return db.query(User).all()
    except Exception as e:
        raise e

def authenticate_user(db: Session, username: str, password: str):
    try:
        user = get_user(db, username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    except Exception as e:
        raise e


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise e


