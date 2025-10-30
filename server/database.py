from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite database URL for storing file metadata
SQLALCHEMY_DATABASE_URL = "sqlite:///./file_data.db"

# Main entry point to database, creating the SQLAlchemy Engine. 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creating session to interact with database for running queries.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all data models to interact.
Base = declarative_base()

# Dependency for getting database session for API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()