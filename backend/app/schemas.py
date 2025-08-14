from __future__ import annotations
from pydantic import BaseModel
from typing import List
from datetime import datetime
from . import models


class SessionBase(BaseModel):
    telegram_id: int
    username: str
    expires_at: datetime

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int


class ConfigBase(BaseModel):
    current_round: int
    current_order_number: int
    max_submissions: int
    submissions_open: bool

class ConfigCreate(ConfigBase):
    pass

class Config(ConfigBase):
    id: int


class UserAlbumSubmissionBase(BaseModel):
    username: str
    album_id: int

class UserAlbumSubmissionCreate(UserAlbumSubmissionBase):
    pass

class UserAlbumSubmission(UserAlbumSubmissionBase):
    id: int


class AlbumBase(BaseModel):
    artist: str
    name: str
    release_year: int
    round_number: int
    order_number: int
    tracks: List["TrackBase"]

class AlbumCreate(AlbumBase):
    pass

class Album(AlbumBase):
    id: int


class TrackBase(BaseModel):
    track_name: str
    album_id: int
    rankings: List["RankingBase"]

class TrackCreate(TrackBase):
    pass

class Track(TrackBase):
    id: int

    class Meta:
        from_attributes = models.Track


class RankingBase(BaseModel):
    username: str
    track_id: int
    placement: int

class RankingCreate(RankingBase):
    pass

class Ranking(RankingBase):
    id: int

    class Meta:
        from_attributes = models.Ranking
