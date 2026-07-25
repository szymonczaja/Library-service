from models import Book, Loan, Member

class LoanRepository: 
    def __init__(self):
        self.loans = []

    def add(self, loan : Loan):
        self.loans.append(loan) 
        
    def get_by_member(self, member_id):
        return [x for x in self.loans if x.member_id == member_id ]
        
    def get_by_book(self, book_id):
        return [x for x in self.loans if x.book_id == book_id]
    
    def get_active_loan(self):
        return [x for x in self.loans if x.is_active()]
    
    def get_overdue(self, current_date):
        return [x for x in self.loans if x.is_overdue(current_date)]

    def get_by_id(self, loan_id):
        for x in self.loans:
            if x.loan_id == loan_id:
                return x
        return None

    def mark_as_returned(self, loan_id, returned_date): 
        loan = self.get_by_id(loan_id)
        if loan:
            loan.returned_date = returned_date

    def update_due_date(self, loan_id, due_date):
        loan = self.get_by_id(loan_id) 
        if loan:
            loan.due_date = due_date
    
class BookRepository:
    def __init__(self):
        self.books = [] 

    def add(self, book: Book):
        self.books.append(book)

    def get_by_id(self, book_id):
        for book in self.books: 
            if book.book_id == book_id: 
                return book 
        return None
    
    def search_by_title(self, phrase):
        return [x for x in self.books if phrase.lower() in x.title.lower()]
    
    def get_all(self): 
        return self.books
    
    def remove(self, book_id):
        book = self.get_by_id(book_id) 
        if book is None: 
            raise ValueError(f'Książka o ID: {book_id} nie istnieje!')
        self.books.remove(book)

class MemberRepository:
    def __init__(self):
        self.members = [] 

    def add(self, member : Member):
        self.members.append(member)

    def get_by_id(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member 
        return None 
    
    def find_by_email(self, email):
        for member in self.members:
            if email == member.email: 
                return member
        return None
    
    def get_all(self):
        return self.members
    
    def remove(self, member_id):
        member = self.get_by_id(member_id) 
        if member is None: 
            raise ValueError(f'Member od ID :{member_id} nie istnieje!')
        self.members.remove(member)