from models import (
    Author, Publisher, Genre, Book, Reader, Librarian, Library
)
from file_manager import (
    save_json, load_json, save_library_to_xml, load_xml,
    library_to_json, library_from_json,  library_from_xml
)
from exceptions import BookNotFoundError, ReaderNotFoundError, NoAvailableCopiesError, OrderNotFoundError

# -------------------- Инициализация библиотеки --------------------

library = Library(name="Моя библиотека")

author1 = Author("Лев Толстой", "Россия")
author2 = Author("Дж. К. Роулинг", "Великобритания")

publisher1 = Publisher("Эксмо", "Москва")
publisher2 = Publisher("Bloomsbury", "Лондон")

genre1 = Genre("Роман")
genre2 = Genre("Фэнтези")

book1 = Book(1, "Война и мир", author1, publisher1, genre1, 1869, 5, "Классика")
book2 = Book(2, "Гарри Поттер и философский камень", author2, publisher2, genre2, 1997, 1, "Фэнтези")

library.add_book(book1, copies=5)
library.add_book(book2, copies=1)

reader1 = Reader(1, "Иван Иванов")
reader2 = Reader(2, "Мария Петрова")
librarian = Librarian(1, "Алексей Смирнов")
library.employees.append(librarian)

librarian.add_reader(library, reader1)
librarian.add_reader(library, reader2)

print("\nБиблиотека успешно инициализирована")
print(f"Всего книг: {len(library.books)} | Читателей: {len(library.readers)} | Сотрудников: {len(library.employees)}\n")

# -------------------- Демонстрация работы исключений --------------------

try:
    # Попытка выдать книгу несуществующему читателю
    library.borrow_book(reader_id=999, book_id=1)
except ReaderNotFoundError as e:
    print(f"Ошибка: {e}")

try:
    # Попытка выдать несуществующую книгу
    library.borrow_book(reader_id=1, book_id=999)
except BookNotFoundError as e:
    print(f"Ошибка: {e}")

# Выдача реальной книги
order1 = library.borrow_book(reader_id=1, book_id=1)
print(f"Выдана книга: {order1}")

try:
    # Попытка выдать книгу, которой больше нет в наличии
    library.borrow_book(reader_id=2, book_id=2)
    library.borrow_book(reader_id=1, book_id=2)
except NoAvailableCopiesError as e:
    print(f"Ошибка: {e}")

# Возврат книги
library.return_book(reader_id=1, book_id=1)
print(f"Читатель {reader1.name} вернул книгу '{book1.title}'")

# Попытка вернуть книгу, которой нет в заказах
try:
    library.return_book(reader_id=1, book_id=999)  # нет такого заказа
except OrderNotFoundError as e:
    print(f"Ошибка: {e}")

# -------------------- Вывод инвентаря --------------------

print("\nТекущий инвентарь:")
librarian.view_inventory(library)

# -------------------- Сохраняем и загружаем --------------------

data_json = library_to_json(library)
save_json("data/library.json", data_json)
print("\nДанные библиотеки сохранены в JSON (data/library.json)")

loaded_data = load_json("data/library.json")
library_copy = library_from_json(loaded_data)
print("Библиотека успешно загружена из JSON")

save_library_to_xml("data/library.xml", library)
print("Данные библиотеки сохранены в XML (data/library.xml)")

loaded_root = load_xml("data/library.xml")
library_copy_from_xml = library_from_xml(loaded_root)
print("Библиотека успешно загружена из XML")

print("\nПроверка загруженных данных из XML:")
for item in library_copy_from_xml.inventory:
    print(f"- {item.book.title} ({item.book.author.name}) — {item.copies} шт.")

print("\nВсе операции успешно выполнены")
