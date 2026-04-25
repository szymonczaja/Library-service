import uuid
from datetime import date
from database import db_init
from sql_repositories import SQLiteBookRepository, SQLiteMemberRepository, SQLiteLoanRepository
from service import LibraryService
from models import Book, Member

conn = db_init('library_database.db')

book_repo = SQLiteBookRepository(conn)
member_repo = SQLiteMemberRepository(conn)
loan_repo = SQLiteLoanRepository(conn)

service = LibraryService(loan_repo, member_repo, book_repo)

book = Book(str(uuid.uuid4()), 'Wiedźmin', 'Andrzej Sapkowski', 1990)
member = Member(str(uuid.uuid4()), 'Jan Kowalski', 'jan@kowalski.pl')

book_repo.add(book)
member_repo.add(member)

loan = service.checkout(book, member, date.today(), date(2026, 5, 25))
print(f'Wypożyczono: {loan}')

stats = service.get_statistics(date.today())
print(f'Statystyki: {stats}')