from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = getenv("DB_PORT", "5432")
DB_PASS = getenv("DB_PASS", "")
DB_USER = getenv("DB_USER", "shade_route")
DB_NAME = getenv("DB_NAME", "shade_route")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/${DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
