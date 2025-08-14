from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import create_db_and_tables, get_session
from . import models
import json

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/albums/{album_id}")
def read_album(album_id: int, session: Session = Depends(get_session)):
    db_album = session.query(models.Album).filter(models.Album.id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album