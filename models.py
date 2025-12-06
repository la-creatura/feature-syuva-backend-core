import sqlite3
import os

DB_NAME = 'db.sqlite'

def get_db_conn():
    db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_conn()
    cursor = conn.cursor()


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    
 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sneakers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        image_url TEXT,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')

   
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("База даних та таблиці перевірено/створено.")

    def add_sneaker(name, description, price, image_url, category_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO sneakers (name, description, price, image_url, category_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, description, price, image_url, category_id))
    conn.commit()
    sneaker_id = cursor.lastrowid
    conn.close()
    return sneaker_id

def get_all_sneakers():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT s.*, c.name as category_name FROM sneakers s
    LEFT JOIN categories c ON s.category_id = c.id
    ''')
    sneakers = cursor.fetchall()
    conn.close()
    return sneakers

def delete_sneaker(sneaker_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sneakers WHERE id = ?', (sneaker_id,))
    conn.commit()
    conn.close()

def get_categories():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    conn.close()
    return categories
    