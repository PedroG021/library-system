import matplotlib.pyplot as plt
import google_books_api as api
from dotenv import load_dotenv
import validators
from models import Book
import storage


def main() -> None:
    load_dotenv()
    print("\nWelcome to your personal library.\n")

    while True:
        try:
            choice = get_menu_choice()
            match choice:
                case 0:
                    print("\nUntil next time\n")
                    return

                case 1:
                    if register_new_book():
                        print("\nBook registered.\n")

                case 2:
                    try:
                        books = list(storage.list_books())
                        if not books:
                            raise RuntimeError("\nError: No books registered yet.\n")

                        else:
                            for book in books:
                                if book:
                                    print(dict_formatter(book), end="")

                        print()

                    except RuntimeError as e:
                        print(e)

                case 3:
                    book_to_search = validators.get_string(
                        "\nWhat is the title of the book you want to search for information? "
                    )
                    if found_book := storage.search_book_by_title(book_to_search):
                        print(dict_formatter(found_book))

                    else:
                        print("\nError: This book was not registered yet.\n")

                case 4:
                    if not generate_graph():
                        print("\nNo books registered yet.\n")

                    else:
                        print("\nGraph generated! Check graphic.png\n")

        except KeyboardInterrupt:
            print("\n\nError: If you want to close the program type '0'\n")

        except EOFError:
            print("\n\nInput closed. Exiting.\n")
            return


def get_menu_choice() -> int:
    while True:
        try:
            print("Type 1 to register a new book.")
            print("Type 2 to list all registered books.")
            print("Type 3 to search for a book by title.")
            print("Type 4 to view a graphic of the available quantity books by genre.")
            print("Type 0 to exit the program.")
            choice = int(
                input("\nWhat do you want to do? Type the corresponding number: ")
            )

        except ValueError:
            print("\nError: Type an integer number like '1' or '2'\n")
            continue

        if 0 <= choice <= 4:
            return choice

        else:
            print("\nError: Invalid number\n")


def register_new_book() -> bool:
    title = validators.get_string("\nWhat is the book's title? ")
    author = validators.get_string("\nWho is the book's author? ")
    genre = None

    if suggestion := api.search_books(title, author):
        print(
            f'\n{suggestion["Title"]}, by {suggestion["Author"]}, of genre: ({suggestion["Genre"]})'
        )

        if validators.get_answer_yes_no(
            "\nIs that the correct book you want to register? y/n "
        ):
            title, author, genre = (
                suggestion["Title"],
                suggestion["Author"],
                suggestion["Genre"],
            )

    if genre is None:
        genre = validators.get_string("\nWhat is the book's genre? ")

    quantity = validators.get_positive_int(
        "\nHow many copies do you want to register? "
    )
    storage.add_book(Book(title, author, genre, quantity).to_dict())
    return True


def dict_formatter(book_dict: dict[str, str]) -> str:
    return f'\nTitle: {book_dict["Title"]} | Author: {book_dict["Author"]} | Genre: {book_dict["Genre"]} | Available Copies: {book_dict["Available quantity"]}\n'


def generate_graph() -> bool | None:
    if genre_quantity_dict := storage.dict_books_by_genre():
        genres = list(genre_quantity_dict.keys())
        quantities = list(genre_quantity_dict.values())
        plt.bar(genres, quantities)
        plt.xticks(rotation=45, ha="right")
        plt.title("Quantity of books by genre", fontsize=14, pad=15)
        plt.xlabel("Genre", fontsize=12, labelpad=20)
        plt.ylabel("Quantity", fontsize=12, labelpad=15)
        plt.grid(axis="y")
        plt.tight_layout()
        plt.savefig("graphic.png")
        plt.close("all")
        return True

    else:
        return None


if __name__ == "__main__":
    main()
