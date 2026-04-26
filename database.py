import sqlite3 
from sqlite3 import Error

def db_init(db_path):
    sql_create_table = '''
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS Book (
        book_id TEXT PRIMARY KEY, 
        title TEXT NOT NULL, 
        author TEXT NOT NULL, 
        year INT NOT NULL
    ); 
    CREATE TABLE IF NOT EXISTS Member ( 
        member_id TEXT PRIMARY KEY, 
        name TEXT NOT NULL, 
        email TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Loan (
        loan_id TEXT PRIMARY KEY, 
        book_id TEXT, 
        member_id TEXT, 
        loan_date TEXT NOT NULL, 
        due_date TEXT NOT NULL, 
        returned_date TEXT,
        FOREIGN KEY (book_id) REFERENCES Book (book_id), 
        FOREIGN KEY (member_id) REFERENCES Member (member_id)
    );
    '''
    try: 
        conn = sqlite3.connect(db_path, check_same_thread=False) 
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON;')
        conn.executescript(sql_create_table)
        return conn 
    except Error as e: 
        print(f'ERROR: {e}')
        return None 
    




