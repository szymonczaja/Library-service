import pytest
from library import Book, Member, LoanRepository, LibraryService, BookRepository, MemberRepository
from datetime import date

@pytest.fixture
def setup():
    loan_repo = LoanRepository()
    book_repo = BookRepository()
    member_repo = MemberRepository()
    library_service = LibraryService(loan_repo, member_repo, book_repo)
    book1 = Book('123231', 'zycie', 'Szymon', 2100)
    book2 = Book('we1234', 'ciepienie', 'Bogdan', 2200)
    member1 = Member('adasdasd', 'Kris', 'kris@gmail.com')
    member2 = Member('afanfafn', 'Woj', 'woj@wp.pl')
    book_repo.add(book1)
    book_repo.add(book2)
    member_repo.add(member1)
    member_repo.add(member2)
    return library_service, loan_repo, member1, book1

def test_checkout_create_loan(setup):
    service, loan_repo, member, book = setup
    loan = service.checkout(book, member, date(2026, 4, 20), date(2026, 5, 20))
    assert loan.is_active() is True 
    assert len(loan_repo.loans) == 1
    assert loan.book_id == book.book_id
    assert loan.member_id == member.member_id 

def test_checkout_raises_when_unavailable(setup):
    service, loan_repo, member, book = setup 
    service.checkout(book, member, date(2026, 4, 20), date(2026, 5, 20))
    with pytest.raises(ValueError):
        service.checkout(book, member, date(2026, 4, 20), date(2026, 5, 20))