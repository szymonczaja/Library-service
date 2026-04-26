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
        if book_ is None:
            raise ValueError('Książka nie istnieje!')
        member_ =  self.member_repo.get_by_id(member_id)
        if member_ is None:
            raise ValueError('Member nie istnieje!')
        return self.checkout(book_, member_, loan_date, due_date)
        

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
        self.loan_repo.mark_as_returned(loan_id, return_date)
        return loan

    def extend_due_date(self, loan_id, new_due_date):
        loan_ = self.loan_repo.get_by_id(loan_id)
        if loan_ is None: 
            raise ValueError(f'Loan id: {loan_id} nie istnieje!')
        if not loan_.is_active():
            raise ValueError('Ksiązka została juz oddana!')
        if loan_.due_date >= new_due_date:
            raise ValueError('Podana data jest nieprawidłowa!')
        loan_.due_date = new_due_date
        self.loan_repo.update_due_date(loan_id, new_due_date)
        return loan_

    def get_overdue_loans(self, current_date):
        overdue_loans = self.loan_repo.get_overdue(current_date)
        return overdue_loans

    def member_history(self, member_id):
        member_loans = self.loan_repo.get_by_member(member_id)
        return sorted(member_loans, key=lambda x: x.loan_date)
    
    def get_member_overdue_loans(self, member_id, current_date):
        member_loans = self.loan_repo.get_by_member(member_id)
        return [loan for loan in member_loans if loan.is_overdue(current_date)]
    
    def get_active_loans_by_member(self, member_id):
        member_loans = self.loan_repo.get_by_member(member_id)
        return [x for x in member_loans if x.is_active()]
    
    def remove_book(self, book_id):
        book_ = self.book_repo.get_by_id(book_id)
        if book_ is None:
            raise ValueError(f'Ksiazka o id: {book_id} nie istnieje!')
        loans_ = self.loan_repo.get_by_book(book_.book_id)
        if any(l.is_active() for l in loans_):
            raise ValueError('Ksiazka wypozyczona! Nie mozna usunac!')
        self.book_repo.remove(book_id)

    def add_book(self, book : Book):
        book_ = self.book_repo.get_by_id(book.book_id)
        if book_ is not None:
            raise ValueError(f'Książka o ID: {book.book_id} już istnieje!')
        self.book_repo.add(book)
        return book

    def remove_member(self, member_id):
        member_ = self.member_repo.get_by_id(member_id)
        if member_ is None:
            raise ValueError(f'Member o id: {member_id} nie istnieje!')
        active_member_loans = self.get_active_loans_by_member(member_id)
        if active_member_loans:
            raise ValueError('Użytkownik ma aktywne wypożyczenia!')
        self.member_repo.remove(member_id)

    def add_member(self, member : Member):
        member_ = self.member_repo.get_by_id(member.member_id)
        if member_ is not None:
            raise ValueError(f'Member o ID: {member.member_id} już istnieje!')
        self.member_repo.add(member)
        return member

    def search_books_by_title(self, phrase):
        return self.book_repo.search_by_title(phrase)
        
    def is_book_available(self, book_id): 
        book_loans = self.loan_repo.get_by_book(book_id)
        for loan in book_loans:
            if loan.is_active():
                return False 
        return True 
    
    def get_statistics(self, current_date):
        return {
            'total_books': len(self.book_repo.get_all()),
            'total_members': len(self.member_repo.get_all()),
            'active_loans': len(self.loan_repo.get_active_loan()),
            'overdue_loans': len(self.loan_repo.get_overdue(current_date))
        }