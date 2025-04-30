from sqlalchemy import create_engine, MetaData
from databases import Database
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()
database = Database(DATABASE_URL)
