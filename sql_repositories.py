from sqlite3 import Error
from models import Book, Member, Loan

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
    def __init__(self):
        pass

    

class SQLiteLoanRepository:
    def __init__(self):
        pass