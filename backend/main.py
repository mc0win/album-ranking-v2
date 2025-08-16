from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import true, and_, update
from .core.database import (
    get_session,
    create_db_and_tables,
    Session,
    Config,
    UserAlbumSubmission,
    Album,
    Track,
    Ranking,
)
from .core.api import processUrl


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:5173",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Album Ranking API"}


@app.get("/albums/")
async def get_albums(
    round_number: int = None,
    artist: str = None,
    name: str = None,
    release_year: int | None = None,
    session: Session = Depends(get_session),
):
    m = Album
    db_albums = (
        session.query(m)
        .where(
            (m.artist == artist) if artist is not None else true(),
            (m.name == name) if name is not None else true(),
            (m.release_year == release_year) if release_year is not None else true(),
            (m.round_number == round_number) if round_number is not None else true(),
        )
        .all()
    )
    if len(db_albums) == 0:
        raise HTTPException(status_code=404, detail="No albums found")
    return db_albums


@app.post("/albums/")
async def create_album(
    source: str,
    url: str,
    session: Session = Depends(get_session),
):
    album = processUrl(source, url)
    artist = album["artist"]
    name = album["name"]
    release_year = album["release_year"]
    for key in ("artist", "name", "release_year"):
        album.pop(key, None)
    tracks = list(album.values())
    config = session.query(Config).first()
    q = session.query(Album)
    if q.where(and_(Album.artist == artist, Album.name == name)).first() is not None:
        raise HTTPException(status_code=500, detail="Album already exist")
    if config.current_round != 1:
        if (
            q.where(
                and_(
                    Album.round_number == config.current_round - 1,
                    Album.artist == artist,
                )
            ).first()
            is not None
        ):
            raise HTTPException(
                status_code=500, detail="Artist was already submitted in the last round"
            )
    previous_album = (
        session.query(Album).where(Album.round_number == config.current_round).all()
    )
    db_album = Album(
        artist=artist,
        name=name,
        release_year=release_year,
        round_number=config.current_round,
        order_number=(
            (previous_album[-1].order_number + 1) if len(previous_album) != 0 else 1
        ),
    )
    session.add(db_album)
    session.commit()
    album_id = (
        session.query(Album)
        .where(Album.artist == artist, Album.name == name)
        .first()
        .id
    )
    db_tracks = []
    for track_name in album.values():
        db_tracks.append(Track(track_name=track_name, album_id=album_id))
    session.add_all(db_tracks)
    session.commit()
    session.refresh(db_album)
    return db_album


@app.get("/albums/{album_id}")
async def get_album(album_id: int, session: Session = Depends(get_session)):
    db_album = session.query(Album).where(Album.id == album_id).first()
    if not db_album:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album


@app.post("/albums/{album_id}")
async def create_ranking(
    album_id: int,
    username: str,
    placements: Annotated[list[int], Query()],
    session: Session = Depends(get_session),
):
    db_album = session.query(Album).where(Album.id == album_id).first()
    tracks = session.query(Track).where(Track.album_id == album_id).all()
    db_rankings = []
    if len(tracks) == 0:
        raise HTTPException(status_code=404, detail="Album not found")
    if len(tracks) != len(placements):
        raise HTTPException(
            status_code=400,
            detail="Amount of placements is not same as amount of tracks in album",
        )
    for i in range(len(placements)):
        db_ranking = Ranking(
            username=username, track_id=tracks[i].id, placement=placements[i]
        )
        db_rankings.append(db_ranking)
    session.add_all(db_rankings)
    session.commit()
    session.refresh(db_album)
    return db_album


@app.get("/tracks/")
async def get_tracks(
    track_name: str = None,
    album_id: int = None,
    session: Session = Depends(get_session),
):
    m = Track
    db_tracks = (
        session.query(m)
        .where(
            (m.track_name == track_name) if track_name is not None else true(),
            (m.album_id == album_id) if album_id is not None else true(),
        )
        .all()
    )
    if len(db_tracks) == 0:
        raise HTTPException(status_code=404, detail="No tracks found")
    return db_tracks


@app.get("/tracks/{track_id}")
async def get_track_info(track_id: int, session: Session = Depends(get_session)):
    db_track = session.query(Ranking).where(Ranking.track_id == track_id).all()
    if len(db_track) == 0:
        raise HTTPException(status_code=404, detail="No rankings found")
    return db_track


@app.get("/config/")
async def get_config(session: Session = Depends(get_session)):
    db_config = session.query(Config).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Config not found")
    return db_config


@app.patch("/config/")
async def change_config(
    current_round: int = None,
    current_order_number: int = None,
    max_submissions: int = None,
    submissions_open: bool = None,
    session: Session = Depends(get_session),
):
    db_config = session.query(Config).first()
    session.execute(
        update(Config),
        [
            {
                "id": db_config.id,
                "current_round": (
                    current_round
                    if current_round is not None
                    else db_config.current_round
                ),
                "current_order_number": (
                    current_order_number
                    if current_order_number is not None
                    else db_config.current_order_number
                ),
                "max_submissions": (
                    max_submissions
                    if max_submissions is not None
                    else db_config.max_submissions
                ),
                "submissions_open": (
                    submissions_open
                    if submissions_open is not None
                    else db_config.submissions_open
                ),
            }
        ],
    )
    session.commit()
    session.refresh(db_config)
    return db_config
