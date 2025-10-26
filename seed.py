import sqlite3

conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

print("Очищення старих даних (якщо є)...")

cursor.execute('DELETE FROM sneakers')
cursor.execute('DELETE FROM categories')

print("Додавання категорій...")
try:
    cursor.execute("INSERT INTO categories (name) VALUES ('Для Бігу')")
    cursor.execute("INSERT INTO categories (name) VALUES ('Лайфстайл')")
    cursor.execute("INSERT INTO categories (name) VALUES ('Для Баскетболу')")
    conn.commit() 
except sqlite3.IntegrityError:
    print("Категорії вже існують.")


cat_run_id = cursor.execute("SELECT id FROM categories WHERE name = 'Для Бігу'").fetchone()[0]
cat_life_id = cursor.execute("SELECT id FROM categories WHERE name = 'Лайфстайл'").fetchone()[0]

print("Додавання товарів...")
try:
    cursor.execute("INSERT INTO sneakers (name, description, price, image_url, category_id) VALUES (?, ?, ?, ?, ?)",
                   ('Nike Air Force 1', 
                    'Класичний білий стиль', 
                    4500, 
                    'https://imgproxy.cdn-tinkoff.ru/t_device_1920_x2/aHR0cHM6Ly9wdWJsaWMtc3RhdGljLnRpbmtvZmZqb3VybmFsLnJ1L2RvbHlhbWUvdXBsb2Fkcy8yMDI1LzA0L3FIcVZqOElkLWNvdmVyLWgucG5n',
                    cat_life_id)
                  )

    cursor.execute("INSERT INTO sneakers (name, description, price, image_url, category_id) VALUES (?, ?, ?, ?, ?)",
                   ('Adidas Superstar', 
                    'Легенда вулиць', 
                    4200, 
                    'https://img.joomcdn.net/d31c53bd95c49e3794030aeaf1872e392e889191_1024_1024.jpeg',
                    cat_life_id)
                  )

    cursor.execute("INSERT INTO sneakers (name, description, price, image_url, category_id) VALUES (?, ?, ?, ?, ?)",
                   ('Nike Pegasus 40', 
                    'Для щоденних пробіжок', 
                    5100, 
                    'https://s.6264.com.ua/section/promonewsintext/upload/images/promo/intext/000/051/384/krosipng_5db97aadb2edb.jpg',
                    cat_run_id)
                  )

    conn.commit() 
    print("Товари та категорії успішно додано!")

except sqlite3.Error as e:
    print(f"Виникла помилка: {e}")
finally:
    conn.close()