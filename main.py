import time
from contextlib import contextmanager

@contextmanager
def timer():
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time:.2f} seconds")

def calculate_product(limit):
    product = 1
    for i in range(1, limit + 1):
        product *= i
    return product

limit = 100000

with timer():
    result = calculate_product(limit)


import sqlite3
import psycopg2

db_name = 'lesson'
password = '1436'
host = 'localhost'
port = 5432
user = 'postgres'

conn = psycopg2.connect(dbname=db_name,
                        password=password,
                        host=host,
                        port=port,
                        user=user)

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("Original table data:")
        self.cursor.execute("SELECT * FROM test")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        print("Modified table data:")
        self.cursor.execute("SELECT * FROM test")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        self.conn.close()

conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, value TEXT)''')
cursor.execute('''DELETE FROM test''')
cursor.executemany('''INSERT INTO test (value) VALUES (?)''', [('A',), ('B',), ('C',)])
conn.commit()
conn.close()

# DatabaseContextManager dan foydalanish
with DatabaseManager('example.db') as cursor:
    cursor.execute("UPDATE test SET value = 'Modified' WHERE value = 'A'")

