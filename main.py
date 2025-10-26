from models import (
    Library, Book, Author, Publisher, Genre, Reader, Librarian, InventoryItem, Order
)
from file_manager import library_to_json, library_from_json

# -------------------- Инициализация библиотеки --------------------

library = Library(name="Моя библиотека")

# --- Создание авторов, издателей и жанров ---
author1 = Author("Лев Толстой", "Россия")
author2 = Author("Дж. К. Роулинг", "Великобритания")

publisher1 = Publisher("Эксмо", "Москва")
publisher2 = Publisher("Bloomsbury", "Лондон")

genre1 = Genre("Роман")
genre2 = Genre("Фэнтези")

# --- Создание книг с категориями ---
book1 = Book(
    book_id=1,
    title="Война и мир",
    author=author1,
    publisher=publisher1,
    genre=genre1,
    year=1869,
    copies=5,
    category="Классика"
)

book2 = Book(
    book_id=2,
    title="Гарри Поттер и философский камень",
    author=author2,
    publisher=publisher2,
    genre=genre2,
    year=1997,
    copies=3,
    category="Фэнтези"
)

library.add_book(book1, copies=book1.copies)
library.add_book(book2, copies=book2.copies)

# --- Создание читателей ---
reader1 = Reader(reader_id=1, name="Иван Иванов")
reader2 = Reader(reader_id=2, name="Мария Петрова")

library.readers.extend([reader1, reader2])

# --- Создание сотрудников ---
librarian = Librarian(employee_id=1, name="Алексей Смирнов")
library.employees.append(librarian)

# -------------------- Работа с библиотекой --------------------

# Выдача книг
order1 = library.borrow_book(reader_id=1, book_id=1)
print(f"Выдана книга: {order1}")

order2 = library.borrow_book(reader_id=2, book_id=2)
print(f"Выдана книга: {order2}")

# Возврат книги
library.return_book(reader_id=1, book_id=1)
print(f"Читатель {reader1.name} вернул книгу '{book1.title}'")

# -------------------- Сохранение в JSON --------------------

data = library_to_json(library)  # только один аргумент
import json
with open("data/library.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Данные библиотеки сохранены в JSON")

# -------------------- Загрузка из JSON --------------------

with open("data/library.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)  # json.load сразу преобразует null -> None

library_copy = library_from_json(loaded_data)
print("Данные библиотеки загружены из JSON")

# Проверка загруженных данных
for book in library_copy.books:
    print(f"Книга: {book.title}, Категория: {book.category}, Автор: {book.author.name}")
