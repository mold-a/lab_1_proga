from datetime import datetime, timedelta
from typing import List, Optional



class Author:
    def __init__(self, name: str, country: str):
        self.name = name
        self.country = country

    def __repr__(self):
        return f"Author(name={self.name}, country={self.country})"

    def to_dict(self) -> dict:
        return {"name": self.name, "country": self.country}

    @classmethod
    def from_dict(cls, data: dict) -> 'Author':
        return cls(data["name"], data["country"])


class Publisher:
    def __init__(self, name: str, country: str):
        self.name = name
        self.country = country

    def __repr__(self):
        return f"Publisher(name={self.name}, country={self.country})"

    def to_dict(self) -> dict:
        return {"name": self.name, "country": self.country}

    @classmethod
    def from_dict(cls, data: dict) -> 'Publisher':
        return cls(data["name"], data["country"])


class Genre:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Genre(name={self.name})"

    def to_dict(self) -> dict:
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> 'Genre':
        return cls(data["name"])


class Book:
    def __init__(self, book_id: int, title: str, author: Author, publisher: Publisher,
                 genre: Genre, year: int, copies: int, category: str):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.genre = genre
        self.year = year
        self.copies = copies
        self.category = category

    def __repr__(self):
        return f"Book(id={self.book_id}, title={self.title})"

    def to_dict(self) -> dict:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author.to_dict(),
            "publisher": self.publisher.to_dict(),
            "genre": self.genre.to_dict(),
            "year": self.year,
            "copies": self.copies,
            "category": self.category  # сериализация строки
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            author=Author.from_dict(data["author"]),
            publisher=Publisher.from_dict(data["publisher"]),
            genre=Genre.from_dict(data["genre"]),
            year=data["year"],
            copies=data["copies"],
            category=data.get("category", "Не указано")  # десериализация строки
        )


class Reader:
    def __init__(self, reader_id: int, name: str):
        self.reader_id = reader_id
        self.name = name

    def __repr__(self):
        return f"Reader(id={self.reader_id}, name={self.name})"

    def to_dict(self) -> dict:
        return {"reader_id": self.reader_id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> 'Reader':
        return cls(data["reader_id"], data["name"])


class Employee:
    def __init__(self, employee_id: int, name: str):
        self.employee_id = employee_id
        self.name = name

    def __repr__(self):
        return f"Employee(id={self.employee_id}, name={self.name})"

    def to_dict(self) -> dict:
        return {"employee_id": self.employee_id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> 'Employee':
        return cls(data["employee_id"], data["name"])

class Category:
    def __init__(self, category_id: int, name: str, description: str = ""):
        self.category_id = category_id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Category(id={self.category_id}, name={self.name})"

    def to_dict(self) -> dict:
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Category':
        return cls(
            category_id=data["category_id"],
            name=data["name"],
            description=data.get("description", "")
        )


class Librarian(Employee):
    """Простейший класс библиотекаря с базовыми действиями"""

    def add_reader(self, library: 'Library', reader: Reader):
        """Просто добавляем читателя без проверки"""
        library.readers.append(reader)

    def add_book(self, library: 'Library', book: Book, copies: int = 1):
        """Добавляем книгу, увеличиваем копии, если она уже есть"""
        inventory_item = next((i for i in library.inventory if i.book.book_id == book.book_id), None)
        if inventory_item:
            inventory_item.copies += copies
        else:
            library.books.append(book)
            library.inventory.append(InventoryItem(book, copies))

    def view_inventory(self, library: 'Library') -> list:
        """Простой просмотр инвентаря"""
        return [(i.book.title, i.copies) for i in library.inventory]


class InventoryItem:
    def __init__(self, book: Book, copies: int):
        self.book = book
        self.copies = copies

    def __repr__(self):
        return f"InventoryItem(book={self.book.title}, copies={self.copies})"

    def to_dict(self) -> dict:
        return {"book": self.book.to_dict(), "copies": self.copies}

    @classmethod
    def from_dict(cls, data: dict) -> 'InventoryItem':
        return cls(Book.from_dict(data["book"]), data["copies"])


class Order:
    def __init__(self, order_id: int, book: Book, reader: Reader,
                 issued_at: Optional[str] = None, due_at: Optional[str] = None,
                 returned_at: Optional[str] = None):
        self.order_id = order_id
        self.book = book
        self.reader = reader
        self.issued_at = issued_at or datetime.utcnow().isoformat()
        self.due_at = due_at or (datetime.utcnow() + timedelta(days=14)).isoformat()
        self.returned_at = returned_at

    def __repr__(self):
        return f"Order #{self.order_id}: book_id={self.book.book_id}, reader_id={self.reader.reader_id}"

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "book": self.book.to_dict(),
            "reader": self.reader.to_dict(),
            "issued_at": self.issued_at,
            "due_at": self.due_at,
            "returned_at": self.returned_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        return cls(
            order_id=data["order_id"],
            book=Book.from_dict(data["book"]),
            reader=Reader.from_dict(data["reader"]),
            issued_at=data.get("issued_at"),
            due_at=data.get("due_at"),
            returned_at=data.get("returned_at")
        )


class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: List[Book] = []
        self.readers: List[Reader] = []
        self.employees: List[Librarian] = []
        self.inventory: List[InventoryItem] = []
        self.orders: List[Order] = []

    def add_book(self, book: Book, copies: int = 1):
        self.books.append(book)
        self.inventory.append(InventoryItem(book, copies))

    def borrow_book(self, reader_id: int, book_id: int) -> Order:
        reader = next((r for r in self.readers if r.reader_id == reader_id), None)
        if not reader:
            from exceptions import ReaderNotFoundError
            raise ReaderNotFoundError(reader_id)

        book = next((b for b in self.books if b.book_id == book_id), None)
        if not book:
            from exceptions import BookNotFoundError
            raise BookNotFoundError(book_id)

        inventory_item = next((i for i in self.inventory if i.book.book_id == book_id), None)
        if inventory_item.copies <= 0:
            from exceptions import NoAvailableCopiesError
            raise NoAvailableCopiesError(book_id)

        inventory_item.copies -= 1
        order_id = len(self.orders) + 1
        order = Order(order_id, book, reader)
        self.orders.append(order)
        return order

    def return_book(self, reader_id: int, book_id: int):
        order = next((o for o in self.orders
                      if o.reader.reader_id == reader_id and
                         o.book.book_id == book_id and
                         o.returned_at is None), None)
        if order:
            order.returned_at = datetime.utcnow().isoformat()
            inventory_item = next((i for i in self.inventory if i.book.book_id == book_id), None)
            if inventory_item:
                inventory_item.copies += 1
