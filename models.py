class Book:
    def __init__(self, title: str, author: str, genre: str, quantity: int) -> None:
        self.title = title
        self.author = author
        self.genre = genre
        self.quantity = quantity

    def to_dict(self) -> dict[str, str | int]:
        return {
            "Title": self.title,
            "Author": self.author,
            "Genre": self.genre,
            "Available quantity": self.quantity,
        }
