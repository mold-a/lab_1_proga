import json
import xml.etree.ElementTree as ET
from typing import Any, List


from models import Book, Author, Publisher, Genre, Reader, Employee, Librarian, InventoryItem, Order, Library


# -------------------- Работа с JSON --------------------

def save_json(filepath: str, data: Any):
    """Сохранение данных в JSON файл"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(filepath: str) -> Any:
    """Загрузка данных из JSON файла"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------- Работа с XML --------------------

def save_xml(filepath: str, root_element: ET.Element):
    """Сохранение данных в XML файл"""
    tree = ET.ElementTree(root_element)
    tree.write(filepath, encoding="utf-8", xml_declaration=True)


def load_xml(filepath: str) -> ET.Element:
    """Загрузка данных из XML файла"""
    tree = ET.parse(filepath)
    return tree.getroot()

import xml.etree.ElementTree as ET
from models import Library, Book, Reader, Librarian, InventoryItem, Order

# -------------------- Сохраняем библиотеку в XML --------------------
def library_to_xml(library: Library) -> ET.Element:
    root = ET.Element("library", name=library.name)

    # книги
    books_el = ET.SubElement(root, "books")
    for book in library.books:
        b_el = ET.SubElement(books_el, "book")
        ET.SubElement(b_el, "book_id").text = str(book.book_id)
        ET.SubElement(b_el, "title").text = book.title
        ET.SubElement(b_el, "author").text = f"{book.author.name} ({book.author.country})"
        ET.SubElement(b_el, "publisher").text = f"{book.publisher.name} ({book.publisher.country})"
        ET.SubElement(b_el, "genre").text = book.genre.name
        ET.SubElement(b_el, "category").text = book.category
        ET.SubElement(b_el, "year").text = str(book.year)
        ET.SubElement(b_el, "copies").text = str(book.copies)

    # читатели
    readers_el = ET.SubElement(root, "readers")
    for reader in library.readers:
        r_el = ET.SubElement(readers_el, "reader")
        ET.SubElement(r_el, "reader_id").text = str(reader.reader_id)
        ET.SubElement(r_el, "name").text = reader.name

    # сотрудники
    employees_el = ET.SubElement(root, "employees")
    for emp in library.employees:
        e_el = ET.SubElement(employees_el, "employee")
        ET.SubElement(e_el, "employee_id").text = str(emp.employee_id)
        ET.SubElement(e_el, "name").text = emp.name

    # инвентарь
    inventory_el = ET.SubElement(root, "inventory")
    for item in library.inventory:
        i_el = ET.SubElement(inventory_el, "item")
        ET.SubElement(i_el, "book_id").text = str(item.book.book_id)
        ET.SubElement(i_el, "copies").text = str(item.copies)

    # заказы
    orders_el = ET.SubElement(root, "orders")
    for order in library.orders:
        o_el = ET.SubElement(orders_el, "order")
        ET.SubElement(o_el, "order_id").text = str(order.order_id)
        ET.SubElement(o_el, "book_id").text = str(order.book.book_id)
        ET.SubElement(o_el, "reader_id").text = str(order.reader.reader_id)
        ET.SubElement(o_el, "issued_at").text = str(order.issued_at)
        ET.SubElement(o_el, "due_at").text = str(order.due_at)
        ET.SubElement(o_el, "returned_at").text = str(order.returned_at) if order.returned_at else ""

    return root


# -------------------- Загружаем библиотеку из XML --------------------
def library_from_xml(root: ET.Element) -> Library:
    library = Library(name=root.attrib.get("name", "Моя библиотека"))

    # книги
    for b_el in root.find("books"):
        author_name, author_country = b_el.find("author").text.split(" (")
        author_country = author_country.rstrip(")")
        publisher_name, publisher_country = b_el.find("publisher").text.split(" (")
        publisher_country = publisher_country.rstrip(")")
        book = Book(
            book_id=int(b_el.find("book_id").text),
            title=b_el.find("title").text,
            author=Author(author_name, author_country),
            publisher=Publisher(publisher_name, publisher_country),
            genre=Genre(b_el.find("genre").text),
            year=int(b_el.find("year").text),
            copies=int(b_el.find("copies").text),
            category=b_el.find("category").text
        )
        library.books.append(book)

    # читатели
    for r_el in root.find("readers"):
        reader = Reader(
            reader_id=int(r_el.find("reader_id").text),
            name=r_el.find("name").text
        )
        library.readers.append(reader)

    # сотрудники
    for e_el in root.find("employees"):
        emp = Librarian(
            employee_id=int(e_el.find("employee_id").text),
            name=e_el.find("name").text
        )
        library.employees.append(emp)

    # инвентарь
    for i_el in root.find("inventory"):
        book_id = int(i_el.find("book_id").text)
        copies = int(i_el.find("copies").text)
        book = next((b for b in library.books if b.book_id == book_id), None)
        if book:
            library.inventory.append(InventoryItem(book, copies))

    # заказы
    for o_el in root.find("orders"):
        book_id = int(o_el.find("book_id").text)
        reader_id = int(o_el.find("reader_id").text)
        book = next((b for b in library.books if b.book_id == book_id), None)
        reader = next((r for r in library.readers if r.reader_id == reader_id), None)
        if book and reader:
            order = Order(
                order_id=int(o_el.find("order_id").text),
                book=book,
                reader=reader,
                issued_at=o_el.find("issued_at").text,
                due_at=o_el.find("due_at").text,
                returned_at=o_el.find("returned_at").text or None
            )
            library.orders.append(order)

    return library


# -------------------- Примеры сериализации/десериализации --------------------

def library_to_json(library: Library) -> dict:
    """Сериализация всей библиотеки в словарь для JSON"""
    return {
        "books": [b.to_dict() for b in library.books],
        "readers": [r.to_dict() for r in library.readers],
        "employees": [e.to_dict() for e in library.employees],
        "inventory": [i.to_dict() for i in library.inventory],
        "orders": [o.to_dict() for o in library.orders]
    }


def library_from_json(data: dict) -> Library:
    """Десериализация библиотеки из словаря JSON"""
    library = Library(name="Моя библиотека")

    for b_data in data.get("books", []):
        library.books.append(Book.from_dict(b_data))  # category теперь учитывается

    for r_data in data.get("readers", []):
        library.readers.append(Reader.from_dict(r_data))

    for e_data in data.get("employees", []):
        library.employees.append(Librarian.from_dict(e_data))

    for i_data in data.get("inventory", []):
        library.inventory.append(InventoryItem.from_dict(i_data))

    for o_data in data.get("orders", []):
        library.orders.append(Order.from_dict(o_data))

    return library


