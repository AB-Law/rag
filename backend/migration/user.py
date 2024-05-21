from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv

from urllib.parse import quote_plus
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.database import dbConfig

# Now instantiate the dbConfig class
dbConfig = dbConfig()

encoded_password = quote_plus(dbConfig.SERVER_PASSWORD.encode('utf-8'))

connection_string = (
    f"postgresql+psycopg2://{dbConfig.SERVER_USERNAME}:{encoded_password}" +
    f"@{dbConfig.SERVER_HOST}:5432/{dbConfig.SERVER_DATABASE}"
)


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Add a new column for user ID
    username = Column(String(50), unique=True)
    full_name = Column(String)
    email = Column(String)
    password = Column(String)
    disabled = Column(Boolean)



engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# this will create the users table
Base.metadata.create_all(bind=engine)