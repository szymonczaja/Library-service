import uuid
from models import Book, Member, Loan 
from repositories import LoanRepository, MemberRepository, BookRepository




class LibraryService:
    def __init__(self, loan_repository : LoanRepository, member_repo : MemberRepository, book_repo : BookRepository): 
        self.loan_repo = loan_repository
        self.member_repo = member_repo
        self.book_repo = book_repo

    def checkout_by_ids(self, book_id : str, member_id, loan_date, due_date):
        book_ = self.book_repo.get_by_id(book_id)
        member_ =  self.member_repo.get_by_id(member_id)
        new_loan = self.checkout(book_, member_, loan_date, due_date)
        return new_loan

    def checkout(self, book : Book, member : Member, loan_date, due_date):
        book_ = self.book_repo.get_by_id(book.book_id)
        if book_ is None:
            raise ValueError('Książka nie istnieje!')
        member_ = self.member_repo.get_by_id(member.member_id)
        if member_ is None:
            raise ValueError('Użytkownik nie istnieje!')
        active_loans = self.loan_repo.get_active_loan()
        for loan in active_loans:
            if loan.book_id == book.book_id:
                raise ValueError(f'Book {book.title} is already loan!')
        new_id = str(uuid.uuid4())
        new_loan = Loan(new_id, book.book_id, member.member_id, loan_date, due_date)
        self.loan_repo.add(new_loan)
        return new_loan
    
    def return_book(self, loan_id, return_date):
        loan = self.loan_repo.get_by_id(loan_id) 
        if loan is None: 
            raise ValueError(f'Brak książki o podanym ID: {loan_id}')
        loan.returned_date = return_date
        return loan 

    def get_overdue_loans(self, current_date):
        overdue_loans = self.loan_repo.get_overdue(current_date)
        return overdue_loans

    def member_history(self, member_id):
        member_loans = self.loan_repo.get_by_member(member_id)
        return sorted(member_loans, key=lambda x: x.loan_date)
    
    def get_member_overdue_loans(self, member_id, current_date):
        member_loans = self.loan_repo.get_by_member(member_id)
        return [loan for loan in member_loans if loan.is_overdue(current_date)]
    
    def is_book_available(self, book_id): 
        book_loans = self.loan_repo.get_by_book(book_id)
        for loan in book_loans:
            if loan.is_active():
                return False 
        return True 