import os
import requests


def search_books(title: str, author: str) -> dict[str, str] | None:
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

    try:
        params = {"q": f'{title} inauthor:"{author}"'}
        if api_key:
            params["key"] = api_key

        r = requests.get(
            "https://www.googleapis.com/books/v1/volumes", params=params, timeout=5
        )

        r.raise_for_status()

        data = r.json()

    except requests.exceptions.RequestException:
        return None

    items = data.get("items")
    if not items:
        return None

    info = items[0]["volumeInfo"]
    categories = info.get("categories") or ["Unknown genre"]

    return {
        "Title": info.get("title", title),
        "Author": ", ".join(info.get("authors", [author])),
        "Genre": categories[0],
    }
