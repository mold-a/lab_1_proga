from models import (
    Author, Publisher, Genre, Book, Reader, Employee, Librarian,
    InventoryItem, Order, Library
)

from file_manager import save_json, load_json, save_xml, load_xml, library_to_json, library_from_json, library_to_xml, \
    library_from_xml

# -------------------- Инициализация библиотеки --------------------

library = Library(name="Моя библиотека")

# Добавляем авторов, издателей, жанры
author1 = Author("Лев Толстой", "Россия")
author2 = Author("Дж. К. Роулинг", "Великобритания")

publisher1 = Publisher("Эксмо", "Москва")
publisher2 = Publisher("Bloomsbury", "Лондон")

genre1 = Genre("Роман")
genre2 = Genre("Фэнтези")

# Добавляем книги
book1 = Book(1, "Война и мир", author1, publisher1, genre1, 1869, 5, "Классика")
book2 = Book(2, "Гарри Поттер и философский камень", author2, publisher2, genre2, 1997, 3, "Фэнтези")

# Добавляем книги в библиотеку
library.add_book(book1, copies=5)
library.add_book(book2, copies=3)

# -------------------- Добавляем читателей --------------------

reader1 = Reader(1, "Иван Иванов")
reader2 = Reader(2, "Мария Петрова")

# Создаём библиотекаря
librarian = Librarian(1, "Алексей Смирнов")
library.employees.append(librarian)

# Библиотекарь добавляет читателей
librarian.add_reader(library, reader1)
librarian.add_reader(library, reader2)

# -------------------- Работаем с заказами --------------------

# Выдача книг
order1 = library.borrow_book(reader_id=1, book_id=1)
order2 = library.borrow_book(reader_id=2, book_id=2)

print(f"Выдана книга: {order1}")
print(f"Выдана книга: {order2}")

# Возврат книги
library.return_book(reader_id=1, book_id=1)
print(f"Читатель {reader1.name} вернул книгу '{book1.title}'")

# -------------------- Сохраняем данные в JSON --------------------

data_json = library_to_json(library)
save_json("data/library.json", data_json)
print("Данные библиотеки сохранены в JSON")

# -------------------- Загружаем данные из JSON --------------------

loaded_data = load_json("data/library.json")
library_copy = library_from_json(loaded_data)
print("Данные библиотеки успешно загружены из JSON")

# -------------------- Сохраняем данные в XML --------------------

root_xml = library_to_xml(library)  # превращаем библиотеку в XML-элемент
save_xml("data/library.xml", root_xml)  # сохраняем в файл
print("Данные библиотеки сохранены в XML")

# -------------------- Загружаем данные из XML --------------------

loaded_root = load_xml("data/library.xml")  # загружаем XML
library_copy_from_xml = library_from_xml(loaded_root)  # десериализуем обратно в Library
print("Данные библиотеки успешно загружены из XML")
