import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config
from starlette.datastructures import Secret

from dotenv import load_dotenv

load_dotenv()

# TODO: Configure your production db
db_username = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_url = f"{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}" 
db_name = os.environ.get('POSTGRES_DB')

connectionString = f'postgresql+psycopg2://{db_username}:{db_password}@{db_url}/{db_name}'

engine = create_engine(connectionString, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')
REFRESH_TOKEN_EXPIRE_MINUTES = os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES')
