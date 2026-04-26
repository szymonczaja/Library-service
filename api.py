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

class CheckoutCreate(BaseModel):
    book_id: str
    member_id: str
    loan_date: date
    due_date: date

class ReturnBookRequest(BaseModel):
    loan_id: str
    return_date: date

class ExtendDueDateRequest(BaseModel):
    loan_id: str
    new_due_date: date

library_service: Optional[LibraryService] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
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

app = FastAPI(description='Library',lifespan=lifespan)

@app.post('/books')
def add_book(book: BookCreate):
    try:
        book_ = Book(book.book_id, book.title, book.author, book.year)
        library_service.add_book(book_)
        return book_
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/books')
def return_all_books():
    return library_service.book_repo.get_all()

@app.get('/books/search')
def search_by_book_title(phrase: str):
    return library_service.search_books_by_title(phrase)


@app.get('/books/{book_id}')
def get_book_by_id(book_id: str):
    book = library_service.book_repo.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail='Książka nie istnieje!')
    return book

@app.delete('/books/{book_id}')
def delete_book(book_id: str):
    try:
        library_service.remove_book(book_id)
        return {'message': 'Książka usunięta pomyślnie!'}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/members')
def add_member(member: MemberCreate):
    try:
        member_ = Member(member.member_id, member.name, member.email)
        library_service.add_member(member_)
        return member_
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/members/{member_id}')
def get_member_by_id(member_id: str):
    member = library_service.member_repo.get_by_id(member_id)
    if member is None:
        raise HTTPException(status_code=404, detail='Member nie istnieje!')
    return member

@app.delete('/members/{member_id}')
def delete_member(member_id: str):
    try:
        library_service.remove_member(member_id)
        return {'message': 'Member usunięty pomyślnie!'}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/checkout')
def checkout(data: CheckoutCreate):
    try:
        loan = library_service.checkout_by_ids(
            data.book_id,
            data.member_id,
            data.loan_date,
            data.due_date
        )
        return loan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/return')
def return_book(data: ReturnBookRequest):
    try:
        loan = library_service.return_book(data.loan_id, data.return_date)
        return loan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/loans/extend')
def extend_due_date(data: ExtendDueDateRequest):
    try:
        loan = library_service.extend_due_date(data.loan_id, data.new_due_date)
        return loan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/loans/active')
def get_active_loans():
    return library_service.loan_repo.get_active_loan()

@app.get('/loans/overdue')
def get_overdue_loans(current_date: date):
    return library_service.get_overdue_loans(current_date)

@app.get('/members/{member_id}/history')
def get_member_history(member_id: str):
    return library_service.member_history(member_id)

@app.get('/members/{member_id}/loans/active')
def get_active_loans_by_member(member_id: str):
    return library_service.get_active_loans_by_member(member_id)

@app.get('/members/{member_id}/loans/overdue')
def get_member_overdue_loans(member_id: str, current_date: date):
    return library_service.get_member_overdue_loans(member_id, current_date)

@app.get('/stats')
def get_stats(current_date: date):
    return library_service.get_statistics(current_date)