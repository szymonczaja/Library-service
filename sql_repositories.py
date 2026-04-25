from sqlite3 import Error
from models import Book, Member, Loan
from datetime import date

class SQLiteBookRepository:
    def __init__(self, conn):
        self.conn = conn

    def add(self, book: Book):
        query = '''
        INSERT INTO Book (book_id, title, author, year)
        VALUES (?, ?, ?, ?)
        '''
        try: 
            cursor = self.conn.cursor()
            data = (book.book_id, book.title, book.author, book.year)
            cursor.execute(query, data)
            self.conn.commit()
        except Error as e: 
            print(f'Error: {e}')

    def get_by_id(self, book_id):
        query = '''
        SELECT book_id, title, author, year FROM Book WHERE book_id = ?
        '''
        try: 
            cursor = self.conn.cursor() 
            cursor.execute(query, (book_id,))
            row = cursor.fetchone()
            if row:
                return Book(book_id=row['book_id'], title=row['title'], author=row['author'], year=row['year'])
            return None
        except Error as e: 
            print(f'ERROR: {e}')
            return None 
        
    def search_by_title(self, phrase):
        query = '''
        SELECT book_id, title, author, year FROM Book WHERE title LIKE ?
        '''
        try: 
            cursor = self.conn.cursor()
            cursor.execute(query, (f'%{phrase}%',))
            rows = cursor.fetchall()
            return [Book(row['book_id'], row['title'], row['author'], row['year']) for row in rows]
        except Error as e:
            print(f'ERROR: {e}')
            return []
        
    def get_all(self): 
        query = '''
        SELECT book_id, title, author, year FROM Book
        '''
        try: 
            cursor = self.conn.cursor() 
            cursor.execute(query)
            rows = cursor.fetchall()
            return [Book(row['book_id'], row['title'], row['author'], row['year']) for row in rows]
        except Error as e:
            print(f'ERROR: {e}')
            return []
        
    def remove(self, book_id):
        query = ''' 
        DELETE FROM Book WHERE book_id = ?
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (book_id,))
            self.conn.commit()
        except Error as e:
            print(f'ERROR: {e}')
            

class SQLiteMemberRepository:
    def __init__(self, conn):
        self.conn = conn 

    def add(self, member: Member):
        query = '''
        INSERT INTO Member (member_id, name, email)
        VALUES (?, ?, ?)
        '''
        try:
            cursor = self.conn.cursor()
            data = (member.member_id, member.name, member.email)
            cursor.execute(query, data)
            self.conn.commit()
        except Error as e: 
            print(f'ERROR: {e}')

    def get_by_id(self, member_id):
        query = '''
        SELECT member_id, name, email from Member WHERE member_id = ?
        '''
        try: 
            cursor = self.conn.cursor()
            cursor.execute(query, (member_id,))
            row = cursor.fetchone()
            if row: 
                return Member(member_id=row['member_id'], name=row['name'], email=row['email'])
            return None
        except Error as e: 
            print(f'ERROR: {e}')

    def find_by_email(self, email):
        query = '''
        SELECT member_id, name, email from Member WHERE email = ?
        '''
        try: 
            cursor = self.conn.cursor()
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if row: 
                return Member(member_id=row['member_id'], name=row['name'], email=row['email'])
            return None
        except Error as e: 
            print(f'ERROR: {e}')

    def get_all(self):
        query = '''
        select member_id, name, email from Member
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [Member(row['member_id'], row['name'], row['email']) for row in rows]
        except Error as e:
            print(f'ERROR: {e}')

    def remove(self, member_id):
        query = '''
        DELETE FROM Member WHERE member_id = ?
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (member_id,))
            self.conn.commit()
        except Error as e:
            print(f'ERROR: {e}')

class SQLiteLoanRepository:
    def __init__(self, conn):
        self.conn = conn 

    def add(self, loan : Loan):
        query = ''' 
        INSERT INTO Loan (loan_id, book_id, member_id, loan_date, due_date, returned_date)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        try:
            cursor = self.conn.cursor()
            data = (loan.loan_id, loan.book_id, loan.member_id, loan.loan_date, loan.due_date, loan.returned_date)
            cursor.execute(query, data)
            self.conn.commit()
        except Error as e:
            print(f'ERROR: {e}')

    def get_by_member(self, member_id):
        query = '''
        SELECT loan_id, book_id, member_id, loan_date, due_date, returned_date
        FROM Loan
        WHERE member_id = ?
        '''
        try: 
            cursor = self.conn.cursor()
            cursor.execute(query, (member_id,))
            rows = cursor.fetchall()
            member_loans = [Loan(row['loan_id'], row['book_id'], row['member_id'], date.fromisoformat(row['loan_date']), date.fromisoformat(row['due_date']), date.fromisoformat(row['returned_date']) if row['returned_date'] else None) for row in rows]
            return member_loans
        except Error as e:
            print(f'ERROR: {e}')

    def get_by_book(self, book_id):
        query = '''
        SELECT loan_id, book_id, member_id, loan_date, due_date, returned_date
        FROM Loan
        WHERE book_id = ?
        '''
        try: 
            cursor = self.conn.cursor()
            cursor.execute(query, (book_id,))
            rows = cursor.fetchall()
            book_loans = [Loan(row['loan_id'], row['book_id'], row['member_id'], date.fromisoformat(row['loan_date']), date.fromisoformat(row['due_date']), date.fromisoformat(row['returned_date']) if row['returned_date'] else None) for row in rows]
            return book_loans
        except Error as e:
            print(f'ERROR: {e}')

    def get_active_loans(self):
        query = '''
        SELECT loan_id, book_id, member_id, loan_date, due_date, returned_date
        FROM Loan
        WHERE returned_date IS NULL
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            active_loans = [Loan(row['loan_id'], row['book_id'], row['member_id'], date.fromisoformat(row['loan_date']), date.fromisoformat(row['due_date']), date.fromisoformat(row['returned_date']) if row['returned_date'] else None) for row in rows]
            return active_loans
        except Error as e:
            print(f'ERROR: {e}')

    def get_overdue_loans(self, current_date):
        query = '''
        SELECT loan_id, book_id, member_id, loan_date, due_date, returned_date
        FROM Loan
        WHERE due_date < ? AND returned_date IS NULL
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            overdue_loans = [Loan(row['loan_id'], row['book_id'], row['member_id'], date.fromisoformat(row['loan_date']), date.fromisoformat(row['due_date']), date.fromisoformat(row['returned_date']) if row['returned_date'] else None) for row in rows]
            return overdue_loans
        except Error as e:
            print(f'ERROR: {e}')

    def get_by_id(self, loan_id):
        query = '''
        SELECT loan_id, book_id, member_id, loan_date, due_date, returned_date
        FROM Loan
        WHERE loan_id = ?
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (loan_id,))
            row = cursor.fetchone()
            return Loan(row['loan_id'], row['book_id'], row['member_id'], date.fromisoformat(row['loan_date']), date.fromisoformat(row['due_date']), date.fromisoformat(row['returned_date']) if row['returned_date'] else None)
        except Error as e:
            print(f'ERROR: {e}')