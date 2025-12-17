from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status

from .auth import AuthVerifier, require_scope
from .config import get_settings
from .models import Book, CreateBook, UpdateBook
from .service import BookService

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.version)

service = BookService()
auth_verifier = AuthVerifier(
    issuer=settings.keycloak_issuer,
    audience=settings.keycloak_audience,
    jwks_url=settings.jwks_url,
)
read_access = require_scope("books:read", auth_verifier)
write_access = require_scope("books:write", auth_verifier)

router_v1 = APIRouter(prefix="/api/v1", tags=["v1"])
router_v2 = APIRouter(prefix="/api/v2", tags=["v2"])


@router_v1.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}


@router_v1.get("/books", response_model=List[Book], dependencies=[Depends(read_access)])
def list_books() -> List[Book]:
    return service.list()


@router_v1.post(
    "/books",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(write_access)],
)
def create_book(payload: CreateBook) -> Book:
    return service.create(payload)


@router_v1.get("/books/{book_id}", response_model=Book, dependencies=[Depends(read_access)])
def get_book(book_id: int) -> Book:
    try:
        return service.get(book_id)
    except KeyError as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") from exc


@router_v1.put(
    "/books/{book_id}",
    response_model=Book,
    dependencies=[Depends(write_access)],
)
def update_book(book_id: int, payload: UpdateBook) -> Book:
    try:
        return service.update(book_id, payload)
    except KeyError as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") from exc


@router_v1.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(write_access)],
)
def delete_book(book_id: int) -> None:
    try:
        service.delete(book_id)
    except KeyError as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") from exc


@router_v2.get("/books", response_model=List[Book], dependencies=[Depends(read_access)])
def list_books_v2() -> List[Book]:
    # Example behavior change: sorted list in v2
    return sorted(service.list(), key=lambda book: book.title.lower())


app.include_router(router_v1)
app.include_router(router_v2)
