
# ==========================================================
# QUIZFLIX - EXTERNAL API ROUTER
# Lab 6: FastAPI Integration
# ==========================================================

from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from backend.app.services.external_api import (
    search_itunes,
    ExternalAPITimeout,
    ExternalAPIError
)


router = APIRouter(
    prefix="/api/external",
    tags=["External API Integration"]
)


# ----------------------------------------------------------
# SEARCH MOVIES, MUSIC AND TV SHOWS
# ----------------------------------------------------------

@router.get("/search")
def search_external_media(

    query: str = Query(
        ...,
        min_length=2,
        max_length=100
    ),

    media: Literal["movie", "music", "tv"] = "movie",

    limit: int = Query(
        default=10,
        ge=1,
        le=50
    )

):

    try:

        return search_itunes(
            query=query,
            media=media,
            limit=limit
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except ExternalAPITimeout as error:

        raise HTTPException(
            status_code=504,
            detail=str(error)
        )

    except ExternalAPIError as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )
