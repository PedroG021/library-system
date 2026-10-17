🇺🇸 English | 🇧🇷 [Português](README.pt-BR.md)

# Personal Library Management System

## Description
A personal library system built with Python that runs directly in the terminal (CLI) to help users organize their books. The application connects to the Google Books API to automatically fetch book details (like titles, authors, and genres) during registration. To keep things simple, it saves data locally in a `storage.jsonl` file for persistence using JSON Lines. It also generates graphs using the Matplotlib library. Finally, the project includes automated tests in `test_project.py` using mocks, so the tests can run independently without messing with the real storage file or depending on the Google API to be online.

---

## Features

- **Automated Data Retrieval**: Consumes the Google Books API to search book details, falling back to manual input upon network or search failures.
- **Data Persistence**: Stores book entries in JSON Lines (`storage.jsonl`). Reads data using a Python generator (`yield`).
- **Data Visualization**: Generates a graphic (`graphic.png`) displaying the number of books available by genre using `matplotlib`.
- **CLI Validation**: The project includes custom validation routines to handle empty strings, numeric option boundaries, and non-positive quantities, so the program does not crash on invalid input.
- **Robust Unit Testing**: Includes a full `pytest` test suite with 32 tests, using `unittest.mock` to test the main functions, isolate file I/O operations and API requests.

---

## File Structure & System Architecture

- **`project.py`**: The entry point of the application. Contains the main CLI loop (`main()`), menu options selection (`get_menu_choice()`), book registration workflow (`register_new_book()`), and graph generation logic (`generate_graph()`).
- **`google_books_api.py`**: Handles external queries to the Google Books API using `requests`. Includes API key fallback handling, and network timeouts (`timeout=5`).
- **`models.py`**: Defines the `Book` data model class, responsible for instantiating book objects and converting internal state into dictionary representations (`to_dict()`).
- **`storage.py`**: The data access layer. Implements file append operations (`add_book`), information generator (`list_books`), dictionary constructor for the Matplotlib library (`dict_books_by_genre`), and book queries (`search_book_by_title`).
- **`validators.py`**: Provides reusable input functions (`get_string`, `get_answer_yes_no`, `get_positive_int`) ensuring defensive input handling and exception handling.
- **`test_project.py`**: The automated test suite for `pytest`. Tests business logic, input validation, storage function, API network, and side effects via `unittest.mock` (`patch`, `mock_open`, `monkeypatch` and `capsys`).
- **`requirements.txt`**: Lists the dependencies required for proper functioning (`requests`, `matplotlib`, `python-dotenv`).
- **`requirements-dev.txt`**: Lists the dependencies required for development and testing (`pytest`, `pytest-cov`, `mypy`, `black`).
- **`.env.example`**: Template for optional Google Books API key. Copy it to `.env` and fill in your key.
- **`storage.example.jsonl`**: Sample data (one book per line) to try the app without registering books first.
- **`.gitignore`**: Keeps local files out of the repository (`.env`, `storage.jsonl`, `graphic.png`, caches).

---

## Design Decisions

1. **Separation of Concerns (SoC)**: Each function was designed to have only one job, making it easier to test. For instance: The storage layer (`storage.py`) contains no direct `print()` calls for data listings, yielding raw dictionaries instead. The presentation layer (`project.py`) is solely responsible for rendering output to the user.
2. **Generators for I/O Handling**: `storage.list_books()` uses `yield` to read the file line by line instead of loading it all at once.
3. **API Defensiveness**: External HTTP requests handle connectivity exceptions (`RequestException`) and HTTP status codes (`raise_for_status()`) internally, ensuring the CLI remains stable even if the API is offline or returns empty responses.
4. **Type Hints**: Every function has type hints, which makes the code easier to read and lets `mypy` catch mistakes.

---

## Setup & Execution

### Prerequisites
- Python 3.11+
- Virtual environment (`venv`)

### Installation

1. **Clone the repository and enter the folder:**
   ```bash
   git clone https://github.com/PedroG021/library-system.git
   cd YOUR-REPOSITORY-NAME
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment:**
   - Linux / macOS:
     ```bash
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     .venv\Scripts\activate
     ```

4. **Install the necessary libraries:**
   ```bash
   pip install -r requirements.txt
   ```

5. **(Optional) Add a Google Books API key.** The app works without one:
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and replace `your_key_here` with your key.

6. **(Optional) Start with sample data.** Otherwise, `storage.jsonl` is created automatically when you register your first book:
   ```bash
   cp storage.example.jsonl storage.jsonl
   ```

### Running the Application

```bash
python project.py
```

### Running Tests

```bash
pip install -r requirements-dev.txt
pytest test_project.py
```

---

## Usage

When you run `python project.py`, a menu is shown:

```text
Type 1 to register a new book.
Type 2 to list all registered books.
Type 3 to search for a book by title.
Type 4 to view a graphic of the available quantity books by genre.
Type 0 to exit the program.
```

The chart from option 4 is saved as `graphic.png` in the current folder.

---

## Known Limitations

- Registering the same book twice creates two separate entries.
- Searching by title requires the exact title (case-insensitive).

---

## Roadmap (v2.0)

Future technical updates planned for this project:

* [ ] Migrate local JSON file persistence to a relational database (**PostgreSQL**) via **SQLAlchemy ORM**.
* [ ] Replace the CLI interface with a RESTful API built using **FastAPI** and **Pydantic** validation schemas.
* [ ] Containerize the application environment using **Docker** and **Docker Compose**.