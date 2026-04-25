from contextlib import asynccontextmanager
from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from database import db_init
from sql_repositories import (
    SQLiteBookRepository,
    SQLiteMemberRepository,
    SQLiteLoanRepository,
)
from models import Book, Member
from service import LibraryService

class BookCreate(BaseModel):
    book_id: str
    title: str
    author: str
    year: int

class MemberCreate(BaseModel):
    member_id: str
    name: str
    email: EmailStr

class CheckoutRequest(BaseModel):
    book_id: str
    member_id: str
    loan_date: date
    due_date: date

class ReturnRequest(BaseModel):
    loan_id: str
    return_date: date

library_service: Optional[LibraryService] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Inicjalizacja bazy, repo i serwisu raz na start aplikacji.
    Zamykanie połączenia przy wyłączaniu. [web:1371]
    """
    global library_service
    conn = db_init("library_database.db")
    book_repo = SQLiteBookRepository(conn)
    member_repo = SQLiteMemberRepository(conn)
    loan_repo = SQLiteLoanRepository(conn)
    library_service = LibraryService(loan_repo, member_repo, book_repo)
    try:
        yield
    finally:
        conn.close()

app = FastAPI(lifespan=lifespan)

