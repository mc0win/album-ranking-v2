from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import true, and_, update
from .core.database import create_db_and_tables, get_session
from .core import models
from .core.api import processUrl

app = FastAPI()

@app.on_event('startup') 
async def on_startup():
    create_db_and_tables()

@app.get('/albums/')
async def get_albums(round_number: int = None, artist: str = None, name: str = None, release_year: int | None = None, session: Session = Depends(get_session)):
    m = models.Album
    db_albums = session.query(m).where(
        (m.artist == artist) if artist is not None else true(), 
        (m.name == name) if name is not None else true(), 
        (m.release_year == release_year) if release_year is not None else true(),
        (m.round_number == round_number) if round_number is not None else true()
    ).all()
    if len(db_albums) == 0:
        raise HTTPException(status_code=404, detail='No albums found')
    return db_albums

@app.post('/albums/')
async def create_album(source: str, url: str, round_number: int, order_number: int, session: Session = Depends(get_session)):
    album = processUrl(source, url)
    artist = album['artist']
    name = album['name']
    release_year = album['release_year']
    for key in ('artist', 'name', 'release_year'):
        album.pop(key, None)
    tracks = list(album.values())
    q = session.query(models.Album)
    if q.where(and_(models.Album.artist == artist, models.Album.name == name)).first() is not None:
        raise HTTPException(status_code=500, detail='Album already exist')
    if q.where(models.Album.order_number == order_number).first() is not None:
        raise HTTPException(status_code=500, detail='Album with same order number already exist')
    db_album = models.Album(artist=artist, name=name, release_year=release_year, round_number=round_number, order_number=order_number)
    session.add(db_album)
    session.commit()
    album_id = session.query(models.Album).where(models.Album.artist == artist, models.Album.name == name).first().id
    db_tracks = []
    for track_name in album.values():
        db_tracks.append(models.Track(track_name=track_name, album_id=album_id))
    session.add_all(db_tracks)
    session.commit()
    session.refresh(db_album)
    return db_album

@app.get('/albums/{album_id}')
async def get_album(album_id: int, session: Session = Depends(get_session)): 
    db_album = session.query(models.Album).where(models.Album.id == album_id).first()
    if not db_album:
        raise HTTPException(status_code=404, detail='Album not found')
    return db_album

@app.post('/albums/{album_id}')
async def create_ranking(album_id: int, username: str, placements: Annotated[list[int], Query()], session: Session = Depends(get_session)):
    db_album = session.query(models.Album).where(models.Album.id == album_id).first()
    tracks = session.query(models.Track).where(models.Track.album_id == album_id).all()
    db_rankings = []
    if len(tracks) == 0:
        raise HTTPException(status_code=404, detail='Album not found')
    if len(tracks) != len(placements):
        raise HTTPException(status_code=400, detail='Amount of placements is not same as amount of tracks in album')
    for i in range(len(placements)):
        db_ranking = models.Ranking(username=username, track_id=tracks[i].id, placement=placements[i])
        db_rankings.append(db_ranking)
    session.add_all(db_rankings)
    session.commit()
    session.refresh(db_album)
    return db_album


@app.get('/tracks/')
async def get_tracks(track_name: str = None, album_id: int = None, session: Session = Depends(get_session)):
    m = models.Track
    db_tracks = session.query(m).where(
        (m.track_name == track_name) if track_name is not None else true(), 
        (m.album_id == album_id) if album_id is not None else true(),
    ).all()
    if len(db_tracks) == 0:
        raise HTTPException(status_code=404, detail='No tracks found')
    return db_tracks

@app.get('/tracks/{track_id}')
async def get_track_info(track_id: int, session: Session = Depends(get_session)):
    db_track = session.query(models.Ranking).where(models.Ranking.track_id == track_id).all()
    if len(db_track) == 0:
        raise HTTPException(status_code=404, detail='No rankings found')
    return db_track


@app.get('/config/')
async def get_config(session: Session = Depends(get_session)):
    db_config = session.query(models.Config).first()
    if not db_config:
        raise HTTPException(status_code=404, detail='Config not found')
    return db_config

@app.patch('/config/')
async def change_config(current_round: int = None, current_order_number: int = None, max_submissions: int = None, submissions_open: bool = None, session: Session = Depends(get_session)):
    db_config = session.query(models.Config).first()
    if not db_config:
        raise HTTPException(status_code=404, detail='Config not found')
    session.execute(
        update(models.Config), 
        [models.Config(
            id=1,
            current_round=(current_round if current_round is not None else db_config.current_round),
            current_order_number=(current_order_number if current_order_number is not None else db_config.current_order_number),
            max_submissions=(max_submissions if max_submissions is not None else db_config.max_submissions),
            submissions_open=(submissions_open if submissions_open is not None else db_config.submissions_open)
        ).__dict__]
    )
    session.commit()
    session.refresh(db_config)
    return db_config