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


