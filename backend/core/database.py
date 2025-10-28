from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    ForeignKey,
    Time,
    DateTime,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session, relationship
from datetime import time
import os
import uuid

users = [
    {"username": "aratorii", "telegram_id": 935125635, "admin_rights": False},
    {"username": "astigm4tism", "telegram_id": 707644429, "admin_rights": False},
    {"username": "Autiat", "telegram_id": 544793092, "admin_rights": False},
    {"username": "Aze", "telegram_id": 1023262053, "admin_rights": False},
    {"username": "belowdecent", "telegram_id": 1107896633, "admin_rights": False},
    {"username": "doriackiy", "telegram_id": 928996843, "admin_rights": False},
    {"username": "HeNCaF", "telegram_id": 1112776659, "admin_rights": False},
    {"username": "Hindeko", "telegram_id": 769816585, "admin_rights": False},
    {"username": "horriblemuck", "telegram_id": 741181098, "admin_rights": False},
    {"username": "Joosenitsa", "telegram_id": 1420576606, "admin_rights": True},
    {"username": "Lemerik", "telegram_id": 996791592, "admin_rights": False},
    {"username": "mcowin", "telegram_id": 5042869688, "admin_rights": False},
    {"username": "morph", "telegram_id": 628535845, "admin_rights": False},
    {"username": "MotokEkb", "telegram_id": 833178165, "admin_rights": False},
    {"username": "MyTaHT_CEBA", "telegram_id": 1297870775, "admin_rights": False},
    {"username": "Nemsyao", "telegram_id": 428081566, "admin_rights": False},
    {"username": "nika", "telegram_id": 1151195486, "admin_rights": False},
    {"username": "noblefoul", "telegram_id": 930347542, "admin_rights": False},
    {"username": "oqua", "telegram_id": 5094942756, "admin_rights": False},
    {"username": "Owleren", "telegram_id": 8196158214, "admin_rights": False},
    {"username": "retsaya", "telegram_id": 1442296055, "admin_rights": False},
    {"username": "sailisy", "telegram_id": 5387114762, "admin_rights": False},
    {"username": "snowy", "telegram_id": 724113434, "admin_rights": False},
    {"username": "tearsfroze", "telegram_id": 413228476, "admin_rights": False},
    {"username": "truelyalyaa", "telegram_id": 912139122, "admin_rights": False},
    {"username": "vomit", "telegram_id": 6777289608, "admin_rights": False},
    {"username": "water667", "telegram_id": 1541527187, "admin_rights": False},
]

Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(32), primary_key=True, default=str(uuid.uuid4()))
    telegram_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    admin_rights = Column(Boolean, nullable=False)

    __table_args__ = (UniqueConstraint("username", "id", name="uix_user_id"),)


class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    current_round = Column(Integer, default=1)
    current_order_number = Column(Integer, default=1)
    max_submissions = Column(Integer, default=2)
    submissions_open = Column(Boolean, default=False)
    max_duration = Column(Time, default=time(hour=2))
    max_tracks = Column(Integer, default=30)
    min_tracks = Column(Integer, default=7)


class UserAlbumSubmission(Base):
    __tablename__ = "user_album_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, autoincrement=True)
    artist = Column(String, nullable=False)
    name = Column(String, nullable=False)
    release_year = Column(Integer)
    duration = Column(Time, nullable=False)
    total_tracks = Column(Integer, nullable=False)
    round_number = Column(Integer, nullable=False)
    cover = Column(String, nullable=False)
    order_number = Column(Integer)

    __table_args__ = (
        UniqueConstraint("round_number", "order_number", name="uix_round_order"),
    )

    tracks = relationship("Track", back_populates="album", cascade="all, delete-orphan")


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    track_name = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)

    album = relationship("Album", back_populates="tracks")
    rankings = relationship(
        "Ranking", back_populates="track", cascade="all, delete-orphan"
    )


class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)
    placement = Column(Integer, nullable=False)
    track = relationship("Track", back_populates="rankings")

    __table_args__ = (UniqueConstraint("username", "track_id", name="uix_user_track"),)


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
    with SessionLocal() as session:
        if session.query(Config).first() is None:
            db_config = Config(id=1)
            session.add(db_config)
            session.commit()
            session.refresh(db_config)
        for user in users:
            if (
                session.query(User)
                .where(User.id == user["telegram_id"])
                .first()
                is None
            ):
                db_user = User(
                    id=user["telegram_id"],
                    username=user["username"],
                    admin_rights=user["admin_rights"],
                )
                session.add(db_user)
                session.commit()
                session.refresh(db_user)
        session.close()
