class LibraryError(Exception):
    """Базовое исключение для библиотеки"""
    pass


class BookNotFoundError(LibraryError):
    """Исключение, когда книга не найдена"""
    def __init__(self, book_id: int):
        super().__init__(f"Книга с ID {book_id} не найдена")


class ReaderNotFoundError(LibraryError):
    """Исключение, когда читатель не найден"""
    def __init__(self, reader_id: int):
        super().__init__(f"Читатель с ID {reader_id} не найден")


class NoAvailableCopiesError(LibraryError):
    """Исключение, когда нет доступных копий книги"""
    def __init__(self, book_id: int):
        super().__init__(f"Нет доступных копий книги с ID {book_id}")


class OrderNotFoundError(LibraryError):
    """Исключение, когда заказ не найден"""
    def __init__(self, order_id: int):
        super().__init__(f"Заказ с ID {order_id} не найден")
