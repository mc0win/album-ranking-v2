from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import relationship
from .database import Base
import uuid

class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(String(32), primary_key=True, default=uuid.uuid4)  # UUID stored as string
    telegram_id = Column(Integer, nullable=False, index=True)
    username = Column(String, nullable=True, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    current_round = Column(Integer, default=1)
    current_order_number = Column(Integer)
    max_submissions = Column(Integer, default=2)
    submissions_open = Column(Boolean, default=False)


class UserAlbumSubmission(Base):
    __tablename__ = 'user_album_submissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=False)


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, autoincrement=True)
    artist = Column(String, nullable=False)
    name = Column(String, nullable=False)
    release_year = Column(Integer)
    round_number = Column(Integer, nullable=False)
    order_number = Column(Integer)

    __table_args__ = (
        UniqueConstraint(
            'round_number', 'order_number', name='uix_round_order'
        ),
    )

    tracks = relationship(
        'Track', back_populates='album', cascade='all, delete-orphan'
    )


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    track_name = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=False)

    album = relationship('Album', back_populates='tracks')
    rankings = relationship(
        'Ranking', back_populates='track', cascade='all, delete-orphan'
    )


class Ranking(Base):
    __tablename__ = 'rankings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    placement = Column(Integer, nullable=False)
    track = relationship('Track', back_populates='rankings')

    __table_args__ = (
        UniqueConstraint('username', 'track_id', name='uix_user_track'),
    )
