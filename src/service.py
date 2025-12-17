from typing import Dict, List

from .models import Book, CreateBook, UpdateBook


class BookService:
    def __init__(self):
        self._store: Dict[int, Book] = {}
        self._next_id = 1

    def reset(self) -> None:
        self._store.clear()
        self._next_id = 1

    def list(self) -> List[Book]:
        return list(self._store.values())

    def create(self, payload: CreateBook) -> Book:
        book = Book(id=self._next_id, **payload.model_dump())
        self._store[self._next_id] = book
        self._next_id += 1
        return book

    def get(self, book_id: int) -> Book:
        if book_id not in self._store:
            raise KeyError(book_id)
        return self._store[book_id]

    def update(self, book_id: int, payload: UpdateBook) -> Book:
        book = self.get(book_id)
        data = book.model_dump()
        for field, value in payload.model_dump(exclude_none=True).items():
            data[field] = value
        data["version"] = book.version + 1
        updated = Book(**data)
        self._store[book_id] = updated
        return updated

    def delete(self, book_id: int) -> None:
        if book_id not in self._store:
            raise KeyError(book_id)
        del self._store[book_id]
