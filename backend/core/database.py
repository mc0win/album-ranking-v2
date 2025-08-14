from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
import os


Base = declarative_base()
db_filename = "app.db"
db_path = os.path.join(os.getcwd(), db_filename)

engine = create_engine(
    f"sqlite:///{db_path}",
    echo=False,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)