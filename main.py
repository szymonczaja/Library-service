from models import Book, Loan, Member
from repositories import LoanRepository, BookRepository, MemberRepository
from service import LibraryService
from datetime import date


def demo():
    book1 = Book('123231', 'zycie', 'Szymon', 2100)
    book2 = Book('we1234', 'ciepienie', 'Bogdan', 2200)
    member1 = Member('adasdasd', 'Kris', 'kris@gmail.com')
    member2 = Member('afanfafn', 'Woj', 'woj@wp.pl')
    member_repo = MemberRepository()
    book_repo = BookRepository()
    loan_repo = LoanRepository()
    library = LibraryService(loan_repo, member_repo, book_repo)
    book_repo.add(book1)
    book_repo.add(book2)
    member_repo.add(member1)
    member_repo.add(member2)
    loan = library.checkout_by_ids('123231', 'adasdasd', date(2026, 4, 1), date(2026, 4, 10))
    print("Wypożyczono:", loan)
    print("\nPrzeterminowane:")
    for l in library.get_overdue_loans(date.today()):
        print(l)

    # historia membera
    print("\nHistoria Krisa:")
    for l in library.member_history('adasdasd'):
        print(l)

demo()