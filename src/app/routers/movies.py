from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from backend.session import create_session
from const import (
    MOVIES_TAGS,
    MOVIES_URL,
    MOVIES_URL_NEW,
)
from schemas.auth import UserSchema
from schemas.movies import MovieSchema
from services.auth import get_current_user
from services.movies import MovieService


router = APIRouter(prefix="/" + MOVIES_URL, tags=MOVIES_TAGS)


@router.get("/", response_model=MovieSchema)
async def get_movie(
    movie_id: int,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> MovieSchema:
    """Get movie by ID."""

    print(user)
    return MovieService(session).get_movie(movie_id)


@router.get("/" + MOVIES_URL_NEW, response_model=List[MovieSchema])
async def get_movies(
    year: int,
    rating: float,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> List[MovieSchema]:
    """Get movies by ``year`` and ``rating``."""
    
    print(user)
    return MovieService(session).get_movies(year, rating)