from models import Book, Author, Publisher, Genre, Reader, Librarian, InventoryItem, Order, Library
from exceptions import *
from file_manager import save_json, load_json, save_xml, load_xml, library_to_json, library_from_json
import xml.etree.ElementTree as ET

# -------------------- Инициализация библиотеки --------------------
library = Library("Городская библиотека")

# Добавляем авторов, издателей, жанры
author1 = Author("Лев Толстой", "Россия")
author2 = Author("Дж. К. Роулинг", "Великобритания")

publisher1 = Publisher("Эксмо", "Москва")
publisher2 = Publisher("Bloomsbury", "Лондон")

genre1 = Genre("Роман")
genre2 = Genre("Фэнтези")

# Добавляем книги
book1 = Book(1, "Война и мир", author1, publisher1, genre1, 1869, 5)
book2 = Book(2, "Гарри Поттер и философский камень", author2, publisher2, genre2, 1997, 3)
library.add_book(book1, copies=5)
library.add_book(book2, copies=3)

# Добавляем читателей
reader1 = Reader(1, "Иван Иванов")
reader2 = Reader(2, "Мария Петрова")
library.readers.extend([reader1, reader2])

# Добавляем библиотекаря
librarian = Librarian(1, "Алексей Смирнов")
library.employees.append(librarian)

# -------------------- Демонстрация выдачи книги --------------------
try:
    order1 = library.borrow_book(reader_id=1, book_id=1)
    print(f"Выдана книга: {order1}")
except (BookNotFoundError, ReaderNotFoundError, NoAvailableCopiesError) as e:
    print(f"Ошибка: {e}")

try:
    order2 = library.borrow_book(reader_id=2, book_id=2)
    print(f"Выдана книга: {order2}")
except (BookNotFoundError, ReaderNotFoundError, NoAvailableCopiesError) as e:
    print(f"Ошибка: {e}")

# -------------------- Возврат книги --------------------
library.return_book(reader_id=1, book_id=1)
print(f"Читатель {reader1.name} вернул книгу '{book1.title}'")

# -------------------- Сохранение в JSON --------------------
json_data = library_to_json(library)
save_json("data/library.json", json_data)
print("Данные библиотеки сохранены в JSON")

# -------------------- Загрузка из JSON --------------------
loaded_data = load_json("data/library.json")
library_copy = library_from_json(loaded_data)
print("Библиотека загружена из JSON")
print(f"Книги: {[book.title for book in library_copy.books]}")

# -------------------- Сохранение в XML --------------------
root = ET.Element("library")
for book in library.books:
    book_elem = ET.SubElement(root, "book", id=str(book.book_id))
    ET.SubElement(book_elem, "title").text = book.title
    ET.SubElement(book_elem, "author").text = book.author.name
    ET.SubElement(book_elem, "publisher").text = book.publisher.name
    ET.SubElement(book_elem, "genre").text = book.genre.name
    ET.SubElement(book_elem, "year").text = str(book.year)
    ET.SubElement(book_elem, "copies").text = str(book.copies)

save_xml("data/library.xml", root)
print("Данные библиотеки сохранены в XML")
