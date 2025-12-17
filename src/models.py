from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float
    in_stock: bool = True
    version: int = 1


class CreateBook(BaseModel):
    title: str
    author: str
    price: float
    in_stock: bool = True


class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None
