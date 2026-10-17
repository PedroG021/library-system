from unittest.mock import patch, mock_open, MagicMock
from project import (
    main,
    get_menu_choice,
    register_new_book,
    generate_graph,
    dict_formatter,
)
import validators
from models import Book
import google_books_api
import requests
import storage

# ===================================================================================================

# MAIN MODULE FUNCTION TESTS (project.py)

# ===================================================================================================


def test_main_case0(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: 0)
    result = main()
    captured = capsys.readouterr()
    assert result is None
    assert "Until next time" in captured.out


def test_main_case1(monkeypatch, capsys):
    entries = iter([1, "The Testing Book", "The Tester", "Fiction", 2, 0])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))
    monkeypatch.setattr(google_books_api, "search_books", lambda *args: None)
    with patch("builtins.open", mock_open()):
        result = main()
        captured = capsys.readouterr()
        assert result is None
        assert "Book registered." in captured.out


def test_main_case2_existing_books(monkeypatch, capsys):
    entries = iter([2, 0])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    mock_books = [
        {
            "Title": "The Frog",
            "Author": "Jeremias",
            "Genre": "Horror",
            "Available quantity": 2,
        },
        {
            "Title": "The Sky",
            "Author": "Skyrunner",
            "Genre": "Adventure",
            "Available quantity": 4,
        },
    ]

    monkeypatch.setattr(storage, "list_books", lambda: iter(mock_books))

    result = main()
    captured = capsys.readouterr()
    assert result is None
    assert (
        "Title: The Frog | Author: Jeremias | Genre: Horror | Available Copies: 2"
        in captured.out
    )
    assert (
        "Title: The Sky | Author: Skyrunner | Genre: Adventure | Available Copies: 4"
        in captured.out
    )


def test_main_case2_no_books(monkeypatch, capsys):
    entries = iter([2, 0])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    monkeypatch.setattr(storage, "list_books", lambda: (x for x in []))

    result = main()
    captured = capsys.readouterr()
    assert result is None
    assert "Error: No books registered yet." in captured.out


def test_main_case3_success(monkeypatch, capsys):
    entries = iter([3, "The Frog", 0])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    monkeypatch.setattr(
        storage,
        "search_book_by_title",
        lambda _: {
            "Title": "The Frog",
            "Author": "Jeremias",
            "Genre": "Horror",
            "Available quantity": 2,
        },
    )

    result = main()
    captured = capsys.readouterr()
    assert result is None
    assert (
        "Title: The Frog | Author: Jeremias | Genre: Horror | Available Copies: 2"
        in captured.out
    )


def test_main_case3_fail(monkeypatch, capsys):
    entries = iter([3, "The Frog", 0])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    monkeypatch.setattr(storage, "search_book_by_title", lambda _: None)

    result = main()
    captured = capsys.readouterr()
    assert result is None
    assert "Error: This book was not registered yet." in captured.out


def test_main_case4(monkeypatch, capsys):
    entries = iter([4, 0])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    monkeypatch.setattr(storage, "dict_books_by_genre", lambda: {"Love": 2})

    mock_plt = MagicMock()
    monkeypatch.setattr("project.plt", mock_plt)

    result = main()
    captured = capsys.readouterr()
    assert "Graph generated! Check graphic.png" in captured.out
    assert result is None


def test_get_menu_choice_using_text(monkeypatch, capsys):
    entries = iter(["hello", 0])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    get_menu_choice()
    captured = capsys.readouterr()
    assert "Error: Type an integer number like '1' or '2'" in captured.out


def test_get_menu_choice_outrange_number(monkeypatch, capsys):
    entries = iter([40, 0])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    get_menu_choice()
    captured = capsys.readouterr()
    assert "Error: Invalid number" in captured.out


def test_register_new_book_with_suggestion(monkeypatch):
    entries = iter(
        ["the midnight library", "matt haig", "ves", "to", "y", 0, "um", "", 3]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    monkey_api_data = {
        "Title": "The Midnight Library",
        "Author": "Matt Haig",
        "Genre": "Fiction",
    }

    monkeypatch.setattr(
        google_books_api, "search_books", lambda title, author: monkey_api_data
    )

    mock_json_file = (
        '{"Title": "The Frog", "Author": "Jeremias", "Genre": "Horror", "Available quantity": 2}\n'
        '{"Title": "The Sky", "Author": "Skyrunner", "Genre": "Adventure", "Available quantity": 4}\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_json_file)):
        result = register_new_book()
        assert result is True


def test_register_new_book_without_suggestion_denying_api(monkeypatch):
    entries = iter(
        ["the midnight library", "matt haig", "n", "", "Romance", 0, -1, "", "two", 2]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    monkey_api_data = {
        "Title": "The Midnight Library",
        "Author": "Matt Haig",
        "Genre": "Fiction",
    }

    monkeypatch.setattr(
        google_books_api, "search_books", lambda title, author: monkey_api_data
    )

    mock_json_file = (
        '{"Title": "The Frog", "Author": "Jeremias", "Genre": "Horror", "Available quantity": 2}\n'
        '{"Title": "The Sky", "Author": "Skyrunner", "Genre": "Adventure", "Available quantity": 4}\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_json_file)):
        result = register_new_book()
        assert result is True


def test_register_new_book_without_suggestion_without_api(monkeypatch):
    entries = iter(
        ["The Crazy Monkey 77", "Jeremias", "", "Adventure", 0, -3, "", "two", 4]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    mock_json_file = (
        '{"Title": "The Frog", "Author": "Jeremias", "Genre": "Horror", "Available quantity": 2}\n'
        '{"Title": "The Sky", "Author": "Skyrunner", "Genre": "Adventure", "Available quantity": 4}\n'
    )

    monkeypatch.setattr(google_books_api, "search_books", lambda title, author: None)

    with patch("builtins.open", mock_open(read_data=mock_json_file)):
        result = register_new_book()
        assert result is True


def test_dict_formatter():
    dict_to_format = {
        "Title": "The frog",
        "Author": "Macarazi",
        "Genre": "Adventure",
        "Available quantity": 2,
    }
    assert (
        dict_formatter(dict_to_format)
        == "\nTitle: The frog | Author: Macarazi | Genre: Adventure | Available Copies: 2\n"
    )


def test_generate_graph_with_mock_plt(monkeypatch):
    monkeypatch.setattr(storage, "dict_books_by_genre", lambda: {"Romance": 2})

    mock_plt = MagicMock()
    monkeypatch.setattr("project.plt", mock_plt)

    result = generate_graph()
    assert result is True
    mock_plt.bar.assert_called_once_with(["Romance"], [2])
    mock_plt.savefig.assert_called_once_with("graphic.png")
    mock_plt.close.assert_called_once_with("all")


def test_generate_graph_no_file_with_mock_plt(monkeypatch):
    monkeypatch.setattr(storage, "dict_books_by_genre", lambda: None)

    result = generate_graph()
    assert result is None


# ====================================================================================================

# BOOK CLASS MODULE TESTS (Book Class - models.py)

# ====================================================================================================


def test_init_book_class():
    book = Book("The Midnight Library", "Matt Haig", "Ficion", 2)

    assert book.title == "The Midnight Library"
    assert book.author == "Matt Haig"
    assert book.genre == "Ficion"
    assert book.quantity == 2


def test_to_dict_from_book_class():
    book_dict = Book.to_dict(Book("The Midnight Library", "Matt Haig", "Fiction", 2))

    assert book_dict == {
        "Title": "The Midnight Library",
        "Author": "Matt Haig",
        "Genre": "Fiction",
        "Available quantity": 2,
    }


# ====================================================================================================

# VALIDATORS MODULE TESTS (validators.py)

# ====================================================================================================


def test_get_string(monkeypatch, capsys):
    entries = iter(["", "The Midnight Library", "", "Matt Haig"])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    title = validators.get_string("\nWhat is the book's title? ")
    captured = capsys.readouterr()
    assert title == "The Midnight Library"
    assert "\nError: the answer cannot be blank." in captured.out

    author = validators.get_string("\nWho is the book's author? ")
    captured = capsys.readouterr()
    assert author == "Matt Haig"
    assert "\nError: the answer cannot be blank." in captured.out


def test_get_answer_yes_no(monkeypatch, capsys):
    entries = iter(["", "si", "yes", "", "nai", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    positive_answer = validators.get_answer_yes_no("s")
    captured = capsys.readouterr()
    assert positive_answer is True
    assert "Error: Answer cannot be blank" in captured.out
    assert "Error: Answer must be 'y | yes' or 'n | no'." in captured.out

    negative_answer = validators.get_answer_yes_no("s")
    captured = capsys.readouterr()
    assert negative_answer is False
    assert "Error: Answer cannot be blank" in captured.out
    assert "Error: Answer must be 'y | yes' or 'n | no'." in captured.out


def test_get_positive_int(monkeypatch, capsys):
    entries = iter(["", "two", -1, 0, 3])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    int_result = validators.get_positive_int("n")
    captured = capsys.readouterr()
    assert int_result == 3
    assert "Error: The quantity must be greater than zero." in captured.out
    assert (
        "Error: The quantity must be entered using a positive integer numbers like '1' or '2'"
        in captured.out
    )


# ====================================================================================================

# GOOGLE BOOKS API MODULE TESTS (google_books_api.py)

# ====================================================================================================


def test_search_books_api_find(monkeypatch):
    mock_response_data = {
        "totalItems": 1,
        "items": [
            {
                "volumeInfo": {
                    "title": "The Midnight Library",
                    "authors": ["Matt Haig"],
                    "categories": ["Fiction"],
                }
            }
        ],
    }

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return mock_response_data

    monkeypatch.setattr(requests, "get", lambda *agrs, **kwargs: MockResponse())

    info = google_books_api.search_books("The Midnight Library", "Matt Haig")
    assert info["Title"] == "The Midnight Library"
    assert info["Author"] == "Matt Haig"
    assert info["Genre"] == "Fiction"


def test_search_books_api_find_total_items_but_no_items(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"totalItems": 1}

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())
    assert google_books_api.search_books("Anything", "Anything") is None


def test_search_books_api_not_find(monkeypatch):
    mock_no_data = {"totalItems": 0}

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return mock_no_data

    monkeypatch.setattr(requests, "get", lambda *agrs, **kwargs: MockResponse())

    info = google_books_api.search_books("The Crazy Monkey 77", "Jeremias")
    assert info is None


def test_search_books_connection_error(monkeypatch):
    def mock_error_data(*args, **kwargs):
        raise requests.exceptions.RequestException

    monkeypatch.setattr(requests, "get", mock_error_data)

    assert google_books_api.search_books("The Crazy Monkey 77", "Jeremias") is None


# ===================================================================================================

# STORAGE MODULE TESTS (storage.py)

# ===================================================================================================


def test_storage_list_books():
    mock_json_file = (
        '{"Title": "The Frog", "Author": "Jeremias", "Genre": "Horror", "Available quantity": 2}\n'
        '{"Title": "The Sky", "Author": "Skyrunner", "Genre": "Adventure", "Available quantity": 4}\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_json_file)):
        result_generator = list(storage.list_books())

    assert list(result_generator) == [
        {
            "Title": "The Frog",
            "Author": "Jeremias",
            "Genre": "Horror",
            "Available quantity": 2,
        },
        {
            "Title": "The Sky",
            "Author": "Skyrunner",
            "Genre": "Adventure",
            "Available quantity": 4,
        },
    ]


def test_storage_list_books_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        assert list(storage.list_books()) == []


def test_storage_list_books_ignore_blank_line():
    mock_json_file = (
        '{"Title": "The Frog", "Author": "Jeremias", "Genre": "Horror", "Available quantity": 2}\n'
        '{"Title": "The Sky", "Author": "Skyrunner", "Genre": "Adventure", "Available quantity": 4}\n'
        "\n"
    )

    with patch("builtins.open", mock_open(read_data=mock_json_file)):
        result_generator = list(storage.list_books())

    assert list(result_generator) == [
        {
            "Title": "The Frog",
            "Author": "Jeremias",
            "Genre": "Horror",
            "Available quantity": 2,
        },
        {
            "Title": "The Sky",
            "Author": "Skyrunner",
            "Genre": "Adventure",
            "Available quantity": 4,
        },
    ]


def test_dict_books_by_genre(monkeypatch):
    mock_jsonl_file = (
        {"Genre": "Love", "Available quantity": 2},
        {"Genre": "Horror", "Available quantity": 1},
    )
    monkeypatch.setattr(storage, "list_books", lambda: mock_jsonl_file)

    result = storage.dict_books_by_genre()
    assert result == {"Love": 2, "Horror": 1}


def test_dict_books_by_genre_sums_same_genre(monkeypatch):
    mock_jsonl_file = (
        {"Genre": "Love", "Available quantity": 2},
        {"Genre": "Love", "Available quantity": 1},
        {"Genre": "Horror", "Available quantity": 1},
    )
    monkeypatch.setattr(storage, "list_books", lambda: mock_jsonl_file)

    result = storage.dict_books_by_genre()
    assert result == {"Love": 3, "Horror": 1}


def test_storage_search_book_by_title():
    mock_json_file = (
        '{"Title": "The Frog", "Author": "Jeremias", "Genre": "Horror", "Available quantity": 2}\n'
        '{"Title": "The Sky", "Author": "Skyrunner", "Genre": "Adventure", "Available quantity": 4}\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_json_file)):
        result = storage.search_book_by_title("The Frog")
        assert result == {
            "Title": "The Frog",
            "Author": "Jeremias",
            "Genre": "Horror",
            "Available quantity": 2,
        }


def test_storage_search_book_by_title_book_not_found():
    mock_json_file = (
        '{"Title": "The Frog", "Author": "Jeremias", "Genre": "Horror", "Available quantity": 2}\n'
        '{"Title": "The Sky", "Author": "Skyrunner", "Genre": "Adventure", "Available quantity": 4}\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_json_file)):
        result = storage.search_book_by_title("The Crazy Monkey 77")

    assert result is None


def test_storage_search_book_by_title_file_doesnt_exist():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = storage.search_book_by_title("The Frog")

    assert result is None


# ===================================================================================================

# TESTS END

# ===================================================================================================
