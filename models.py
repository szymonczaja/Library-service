from dataclasses import dataclass, field
from datetime import date 

@dataclass
class Book:
    book_id : str
    title : str
    author : str
    year : int

    def __repr__(self):
        return f'Book ID: {self.book_id}; Title: {self.title}; Author: {self.author}; Year: {self.year}'

@dataclass
class Member:
    member_id : str
    name : str
    email : str

    def __post_init__(self):
        if '@' not in self.email or '.' not in self.email:
            raise ValueError(f'Nieprawidłowy adres email: {self.email}')
    
    def __repr__(self):
        return f'Member ID: {self.member_id}; Name: {self.name}; Email: {self.email}'
    
@dataclass
class Loan:
    loan_id : str
    book_id : str
    member_id : str
    loan_date : date
    due_date : date  
    returned_date : date = field(default=None)

    def is_active(self):
        return self.returned_date is None 
    
    def is_overdue(self, current_date):
        return True if self.due_date < current_date and self.returned_date is None else False 
    
    def __repr__(self):
        return f"Loan ID: {self.loan_id}; Book ID: {self.book_id}; Member ID: {self.member_id}; Loan Date: {self.loan_date}; Due Date: {self.due_date}; Returned {self.returned_date if self.returned_date else 'No'}"
        