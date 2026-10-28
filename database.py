from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', '5432')
USER = os.getenv('USER', 'user')
DB_NAME = os.getenv('DB_NAME', 'db')
PASSWORD = os.getenv('PASSWORD', 'password')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    # Default to SQLite for local development so the app can start without a Postgres service.
    DATABASE_URL = 'sqlite:///./pagination.db'
else:
    # Use the driver SQLAlchemy expects for Postgres when a full URL is supplied.
    if DATABASE_URL.startswith('postgresql://'):
        DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg2://', 1)

engine_kwargs = {}
if DATABASE_URL.startswith('sqlite'):
    engine_kwargs['connect_args'] = {'check_same_thread': False}

engine = create_engine(DATABASE_URL, **engine_kwargs)

Base = declarative_base()

local_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()