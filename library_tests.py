import pytest
from datetime import date
from models import Book, Loan, Member
from repositories import LoanRepository, MemberRepository, BookRepository
from service import LibraryService

@pytest.fixture
def service():
    loan_repo = LoanRepository()
    member_repo = MemberRepository()
    book_repo = BookRepository()
    return LibraryService(loan_repo, member_repo, book_repo)

def test_checkout_success(service):
    book = Book('121212', 'wiedzmin', 'sapkowski', 2000)
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    service.member_repo.add(member)
    service.book_repo.add(book) 
    loan = service.checkout(book, member, date(2012, 1, 1), date(2012, 3, 3))
    active_loans = service.loan_repo.get_active_loan()
    assert loan.book_id == book.book_id
    assert loan.member_id == member.member_id
    assert loan.loan_date == date(2012, 1, 1)
    assert loan.due_date == date(2012, 3, 3)
    assert len(active_loans) == 1
    assert loan in active_loans

def test_checkout_book_not_exists(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.member_repo.add(member) 
    with pytest.raises(ValueError):
        service.checkout(book, member, date(2026, 2, 3), date(2026, 5, 5))

def test_checkout_member_not_exists(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.book_repo.add(book)
    with pytest.raises(ValueError):
        service.checkout(book, member, date(2024, 1, 1), date(2025, 2, 2))

def test_checkout_book_already_loaned(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    member2 = Member('14444', 'Paul', 'paul_richards@wp.pl')
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.member_repo.add(member)
    service.member_repo.add(member2)
    service.book_repo.add(book)
    service.checkout(book, member, date(2025, 1, 1), date(2026, 1, 1))
    with pytest.raises(ValueError):
        service.checkout(book, member2, date(2025, 6, 6), date(2026, 7, 7))

def test_return_book_success(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.member_repo.add(member)
    service.book_repo.add(book)
    loan = service.checkout(book, member, date(2025, 1, 1), date(2026, 1, 1))
    service.return_book(loan.loan_id, date(2026, 1, 1))
    active_loans = service.loan_repo.get_active_loan()
    assert loan.returned_date == date(2026, 1, 1)
    assert not loan.is_active() 
    assert loan not in active_loans

def test_return_book_invalid_loan_id(service):
    with pytest.raises(ValueError):
        service.return_book('12321321', date(2026, 1, 1))

def test_extend_due_date_success(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.member_repo.add(member)
    service.book_repo.add(book)
    loan = service.checkout(book, member, date(2025, 1, 1), date(2026, 1, 1))
    service.extend_due_date(loan.loan_id, date(2027, 2, 2))
    assert loan.due_date == date(2027, 2, 2)

def test_extend_due_date_loan_not_exists(service):
    with pytest.raises(ValueError):
        service.extend_due_date('19878', date(2028, 1, 1))

def test_extend_due_date_book_already_returned(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.member_repo.add(member)
    service.book_repo.add(book)
    loan = service.checkout(book, member, date(2025, 1, 1), date(2026, 1, 1))
    service.return_book(loan.loan_id, date(2026, 2, 2))
    with pytest.raises(ValueError):
        service.extend_due_date(loan.loan_id, date(2026, 3, 2))

def test_extend_due_date_invalid_new_date(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.member_repo.add(member)
    service.book_repo.add(book)
    loan = service.checkout(book, member, date(2025, 1, 1), date(2026, 1, 1))
    with pytest.raises(ValueError):
        service.extend_due_date(loan.loan_id, date(2024, 1, 1))

def test_is_book_available_true(service):
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.book_repo.add(book)
    assert service.is_book_available(book.book_id)

def test_is_book_available_false(service):
    book = Book('13123213', 'Qwerty', 'John', 2026)
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    service.member_repo.add(member)
    service.book_repo.add(book)
    service.checkout(book, member, date(2025, 1, 1), date(2026, 1, 1))
    assert not service.is_book_available(book.book_id)

def test_remove_book_success(service):
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.book_repo.add(book)
    service.remove_book(book.book_id)
    assert service.book_repo.get_by_id(book.book_id) is None

def test_remove_book_not_exists(service):
    with pytest.raises(ValueError):
        service.remove_book('123123')

def test_remove_book_active_loan(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.member_repo.add(member)
    service.book_repo.add(book)
    service.checkout(book, member, date(2025, 1, 1), date(2026, 1, 1))
    with pytest.raises(ValueError):
        service.remove_book(book.book_id)

def test_remove_member(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    service.member_repo.add(member)
    service.remove_member(member.member_id)
    assert service.member_repo.get_by_id(member.member_id) is None 

def test_remove_member_not_exists(service):
    with pytest.raises(ValueError):
        service.remove_member('99999')

def test_remove_member_active_loan(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    book = Book('13123213', 'Qwerty', 'John', 2026)
    service.member_repo.add(member)
    service.book_repo.add(book)
    service.checkout(book, member, date(2025, 1, 1), date(2026, 1, 1))
    with pytest.raises(ValueError):
        service.remove_member(member.member_id)

def test_get_statistics_empty(service):
    result = service.get_statistics(date(2026, 2, 2))
    assert result['total_books'] == 0
    assert result['total_members'] == 0
    assert result['active_loans'] == 0
    assert result['overdue_loans'] == 0

def test_get_statistics_with_data(service):
    member = Member('131313', 'Szymon', 'szymi@gmail.com')
    book = Book('13123213', 'Qwerty', 'John', 2026)
    book2 = Book('122122', 'Super', 'Jack', 2011)
    service.member_repo.add(member)
    service.book_repo.add(book)
    service.book_repo.add(book2)
    service.checkout(book, member, date(2025, 1, 1), date(2026, 1, 1))
    result = service.get_statistics(date(2026, 3, 3))
    assert result['total_books'] == 2
    assert result['total_members'] == 1
    assert result['active_loans'] == 1
    assert result['overdue_loans'] == 1
    