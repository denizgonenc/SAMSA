from fastapi import HTTPException
from typing import Optional, List
# from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas, exceptions


class MovieCRUD:

    LIMIT = 100
    OFFSET = 0

    # movie's name
    # movie's date of publish // you can add it later. For now adding only name with full text search is enough.
    # movie's director // you can also add this later.

    def list_movie(db: Session, name: Optional[str] = None, offset: int = OFFSET, limit: int = LIMIT) -> List[models.MovieDB]:
        return db.query(models.MovieDB).offset(offset).limit(limit).all()

    def get_movie(db: Session, id: int) -> models.MovieDB:
        db_movie = db.query(models.MovieDB).get(id)
        if not db_movie:
            raise HTTPException(status_code=404, detail="Not Found")
        return db_movie

    def create_movie(db: Session, movie_name: str) -> models.MovieDB:
        if db.query(models.MovieDB).where(models.MovieDB.name == movie_name).first() != None:
            raise exceptions.DuplicateMovieError(movie_name)
        db_movie = models.MovieDB(name=movie_name, date=None, description=None)
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie

    def update_movie(db: Session, movie: schemas.Movie) -> models.MovieDB:
        db_movie = db.query(models.MovieDB).get(movie.id)
        if not db_movie:
            raise HTTPException(status_code=404, detail="Not found")
        movie_data = movie.dict(exclude_unset=True)
        for key, value in movie_data.items():
            setattr(db_movie, key, value)
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    
    def delete_movie(db: Session, id: int) -> int:
        db_movie = db.query(models.MovieDB).get(id)
        db.delete(db_movie)
        db.commit()
        return id