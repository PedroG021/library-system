import json
from collections.abc import Iterator

STORAGE_FILE = "storage.jsonl"


def add_book(book_dict: dict[str, str | int]) -> None:
    with open(STORAGE_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(book_dict, ensure_ascii=False) + "\n")


def list_books() -> Iterator[dict]:
    try:
        with open(STORAGE_FILE, encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    yield json.loads(line)

    except FileNotFoundError:
        return


def dict_books_by_genre() -> dict[str, int]:
    total_books_by_genre_dict: dict[str, int] = {}

    for book_dict in list_books():
        if not book_dict["Genre"] in total_books_by_genre_dict:
            total_books_by_genre_dict[book_dict["Genre"]] = book_dict[
                "Available quantity"
            ]

        else:
            total_books_by_genre_dict[book_dict["Genre"]] += book_dict[
                "Available quantity"
            ]

    return total_books_by_genre_dict


def search_book_by_title(book_name: str) -> dict | None:
    for book in list_books():
        if book["Title"].lower() == book_name.lower():
            return book
    return None
