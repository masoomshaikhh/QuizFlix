
# ==========================================================
# QUIZFLIX - EXTERNAL ENTERTAINMENT API SERVICE
# Lab 6: External API Integration
# API: Apple iTunes Search API
# Library: Requests
# ==========================================================

import requests


ITUNES_SEARCH_URL = "https://itunes.apple.com/search"


class ExternalAPITimeout(Exception):
    """Raised when the external API request times out."""
    pass


class ExternalAPIError(Exception):
    """Raised when the external API request fails."""
    pass


# ----------------------------------------------------------
# SEARCH EXTERNAL ENTERTAINMENT CONTENT
# ----------------------------------------------------------

def search_itunes(
    query: str,
    media: str = "movie",
    limit: int = 10
) -> dict:

    # Map QuizFlix media types to iTunes API parameters.
    media_options = {
        "movie": {
            "media": "movie",
            "entity": "movie"
        },
        "music": {
            "media": "music",
            "entity": "song"
        },
        "tv": {
            "media": "tvShow",
            "entity": "tvSeason"
        }
    }

    if media not in media_options:
        raise ValueError("Unsupported media type.")

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not 1 <= limit <= 50:
        raise ValueError("Result limit must be between 1 and 50.")

    parameters = {
        "term": query.strip(),
        "country": "US",
        "media": media_options[media]["media"],
        "entity": media_options[media]["entity"],
        "limit": limit,
        "lang": "en_us",
        "explicit": "No"
    }

    try:

        response = requests.get(
            ITUNES_SEARCH_URL,
            params=parameters,
            timeout=10,
            headers={
                "User-Agent": "QuizFlix/1.0"
            }
        )

        response.raise_for_status()

    except requests.Timeout as error:

        raise ExternalAPITimeout(
            "External API request timed out."
        ) from error

    except requests.RequestException as error:

        raise ExternalAPIError(
            "Unable to connect to the external API."
        ) from error

    # ------------------------------------------------------
    # PROCESS JSON RESPONSE
    # ------------------------------------------------------

    try:

        data = response.json()

    except ValueError as error:

        raise ExternalAPIError(
            "External API returned invalid JSON."
        ) from error

    if not isinstance(data, dict):
        raise ExternalAPIError(
            "Unexpected response format from external API."
        )

    results = data.get("results", [])

    if not isinstance(results, list):
        raise ExternalAPIError(
            "Invalid results received from external API."
        )

    # ------------------------------------------------------
    # EXTRACT USEFUL INFORMATION
    # ------------------------------------------------------

    formatted_results = []

    for item in results:

        formatted_results.append({

            "id": (
                item.get("trackId")
                or item.get("collectionId")
                or item.get("artistId")
            ),

            "title": (
                item.get("trackName")
                or item.get("collectionName")
                or item.get("artistName")
                or "Unknown Title"
            ),

            "artist": item.get("artistName"),

            "album": item.get("collectionName"),

            "release_date": item.get("releaseDate"),

            "genre": item.get("primaryGenreName"),

            "artwork_url": item.get("artworkUrl100"),

            "store_url": (
                item.get("trackViewUrl")
                or item.get("collectionViewUrl")
            ),

            "description": (
                item.get("longDescription")
                or item.get("shortDescription")
            ),

            "duration_ms": item.get("trackTimeMillis")

        })

    # ------------------------------------------------------
    # RETURN STRUCTURED RESPONSE
    # ------------------------------------------------------

    return {

        "success": True,

        "query": query,

        "media_type": media,

        "result_count": data.get(
            "resultCount",
            len(formatted_results)
        ),

        "results": formatted_results

    }
