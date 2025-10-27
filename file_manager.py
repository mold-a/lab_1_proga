import json
import xml.etree.ElementTree as ET
from typing import Any
from models import Book, Author, Publisher, Genre, Reader, Employee, Librarian, InventoryItem, Order, Library


# -------------------- JSON --------------------

def save_json(filepath: str, data: Any):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_json(filepath: str) -> Any:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------- XML --------------------

def find_by_id(collection, attr, value):
    return next((obj for obj in collection if getattr(obj, attr) == value), None)

def library_to_xml(library: Library) -> ET.Element:
    root = ET.Element("library", name=library.name)

    books_el = ET.SubElement(root, "books")
    for book in library.books:
        b_el = ET.SubElement(books_el, "book")
        for tag, val in {
            "book_id": book.book_id,
            "title": book.title,
            "author": f"{book.author.name} ({book.author.country})",
            "publisher": f"{book.publisher.name} ({book.publisher.country})",
            "genre": book.genre.name,
            "category": book.category,
            "year": book.year,
            "copies": book.copies
        }.items():
            ET.SubElement(b_el, tag).text = str(val)

    readers_el = ET.SubElement(root, "readers")
    for r in library.readers:
        ET.SubElement(readers_el, "reader", id=str(r.reader_id)).text = r.name

    employees_el = ET.SubElement(root, "employees")
    for e in library.employees:
        ET.SubElement(employees_el, "employee", id=str(e.employee_id)).text = e.name

    inventory_el = ET.SubElement(root, "inventory")
    for i in library.inventory:
        item_el = ET.SubElement(inventory_el, "item")
        ET.SubElement(item_el, "book_id").text = str(i.book.book_id)
        ET.SubElement(item_el, "copies").text = str(i.copies)

    orders_el = ET.SubElement(root, "orders")
    for o in library.orders:
        order_el = ET.SubElement(orders_el, "order")
        for tag, val in {
            "order_id": o.order_id,
            "book_id": o.book.book_id,
            "reader_id": o.reader.reader_id,
            "issued_at": o.issued_at,
            "due_at": o.due_at,
            "returned_at": o.returned_at or ""
        }.items():
            ET.SubElement(order_el, tag).text = str(val)

    return root

def save_library_to_xml(filepath: str, library: Library):
    tree = ET.ElementTree(library_to_xml(library))
    tree.write(filepath, encoding="utf-8", xml_declaration=True)

def load_xml(filepath: str) -> ET.Element:
    return ET.parse(filepath).getroot()

def library_from_xml(root: ET.Element) -> Library:
    library = Library(name=root.attrib.get("name", "Моя библиотека"))

    for b in root.find("books"):
        author_name, author_country = b.find("author").text.split(" (")
        publisher_name, publisher_country = b.find("publisher").text.split(" (")
        book = Book(
            int(b.find("book_id").text),
            b.find("title").text,
            Author(author_name, author_country.rstrip(")")),
            Publisher(publisher_name, publisher_country.rstrip(")")),
            Genre(b.find("genre").text),
            int(b.find("year").text),
            int(b.find("copies").text),
            b.find("category").text
        )
        library.books.append(book)

    for r in root.find("readers"):
        library.readers.append(Reader(int(r.attrib["id"]), r.text))

    for e in root.find("employees"):
        library.employees.append(Librarian(int(e.attrib["id"]), e.text))

    for i in root.find("inventory"):
        book = find_by_id(library.books, "book_id", int(i.find("book_id").text))
        if book:
            library.inventory.append(InventoryItem(book, int(i.find("copies").text)))

    for o in root.find("orders"):
        book = find_by_id(library.books, "book_id", int(o.find("book_id").text))
        reader = find_by_id(library.readers, "reader_id", int(o.find("reader_id").text))
        if book and reader:
            library.orders.append(Order(
                int(o.find("order_id").text),
                book, reader,
                o.find("issued_at").text,
                o.find("due_at").text,
                o.find("returned_at").text or None
            ))

    return library


# -------------------- JSON Conversion --------------------

def library_to_json(library: Library) -> dict:
    return {
        "books": [b.to_dict() for b in library.books],
        "readers": [r.to_dict() for r in library.readers],
        "employees": [e.to_dict() for e in library.employees],
        "inventory": [i.to_dict() for i in library.inventory],
        "orders": [o.to_dict() for o in library.orders]
    }

def library_from_json(data: dict) -> Library:
    lib = Library("Моя библиотека")
    for b in data.get("books", []): lib.books.append(Book.from_dict(b))
    for r in data.get("readers", []): lib.readers.append(Reader.from_dict(r))
    for e in data.get("employees", []): lib.employees.append(Librarian.from_dict(e))
    for i in data.get("inventory", []): lib.inventory.append(InventoryItem.from_dict(i))
    for o in data.get("orders", []): lib.orders.append(Order.from_dict(o))
    return lib
