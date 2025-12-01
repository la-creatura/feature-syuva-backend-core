# Звіт з лабораторної роботи 4

## Реалізація бази даних для вебпроєкту

### Інформація про команду
- Назва команди: **Rastik**
  - Морозюк Микола Володимирович(frontend)
  - Сюйва Дмитро Русланович (backend)
  - Гринишин Микола Сергійович (team-leader/frontend)
  - Бугайчук Дмитро Петрович (frontend)
  - Гапяк Марк Вікторович (backend)

## Завдання

### Обрана предметна область

Обрано предметну область **інтернет-магазину кросівок ("Світ Кросівок")**.

Для роботи застосунку потрібно зберігати дані про:
1.  **Товари:** Назва, опис, ціна, фото (таблиця `sneakers`).
2.  **Відгуки користувачів:** Ім'я, email та повідомлення (таблиця `feedback`).
3.  **Категорії товарів:** Назва категорії (таблиця `categories`).

### Реалізовані вимоги

Вкажіть, які рівні завдань було виконано:

- [x] **Рівень 1:** Створено базу даних SQLite (`db.sqlite`) з таблицями для відгуків (`feedback`) та товарів (`sneakers`). Реалізовано базові CRUD операції (Create/Read/Delete) для відгуків. Створено адмін-панель (`/admin`) для перегляду та видалення відгуків.
- [x] **Рівень 2:** Створено додаткову таблицю `categories`, релевантну предметній області. Реалізовано повну роботу з новою таблицею через адмін-панель (створення та видалення категорій). Інтегровано функціональність у застосунок (фільтрація товарів за категоріями).
- [x] **Рівень 3:** Розширено функціональність двома додатковими функціями, що суттєво покращують користувацький досвід:
    1.  **Система пошуку:** Додано форму пошуку, яка дозволяє шукати товари за назвою або описом.
    2.  **Кошик:** Реалізовано кошик для покупок на базі сесій (`session`), що дозволяє додавати товари, переглядати вміст кошика та очищувати його.

## Хід виконання роботи

### Підготовка середовища розробки

- **Версія Python:** 3.13.9 (або 3.14.0, залежно від вашого середовища)
- **Встановлені бібліотеки:** `Flask` (для вебсервера, маршрутизації та сесій).
- **Інші використані інструменти:** Вбудована бібліотека `sqlite3` для прямої роботи з базою даних, `Visual Studio Code` (редактор коду).

### Структура проєкту

Структура файлів відповідає узгодженій архітектурі з розділенням логіки:

```
labwork2-3/ 
├── app.py (Головний файл запуску, налаштування Flask) 
├── models.py (Функції для роботи з БД: init_db, get_db_conn) 
├── routes/ 
│ ├── init.py (Порожній, для пакету Python) 
│ ├── admin.py (Логіка для /admin: відгуки, категорії)
│ ├── feedback.py (Логіка для /feedback) 
│ └── shop.py (Логіка для /, /about, /category, /search, /cart) 
├── templates/ 
│ ├── base.html (Базовий шаблон) 
│ ├── admin.html (Шаблон адмін-панелі відгуків) 
│ ├── admin_categories.html (Шаблон адмін-панелі категорій) 
│ ├── feedback.html (Шаблон форми відгуків)
│ ├── home.html (Головний шаблон для каталогу/пошуку) 
│ ├── about.html (Шаблон "Про нас") 
│ └── cart.html (Шаблон кошика) 
├── db.sqlite (Файл бази даних) 
└── seed.py (Скрипт для початкового заповнення БД)
```

### Проектування бази даних

#### Схема бази даних

Опишіть структуру вашої бази даних:

```
Таблиця "categories":
id (INTEGER, PRIMARY KEY AUTOINCREMENT)
name (TEXT, NOT NULL, UNIQUE)

Таблиця "sneakers" (для товарів):
id (INTEGER, PRIMARY KEY AUTOINCREMENT)
name (TEXT, NOT NULL)
description (TEXT)
price (INTEGER, NOT NULL)
image_url (TEXT)
category_id (INTEGER, FOREIGN KEY REFERENCES categories(id))

Таблиця "feedback" (для відгуків):
id (INTEGER, PRIMARY KEY AUTOINCREMENT)
user_name (TEXT, NOT NULL)
email (TEXT, NOT NULL)
message (TEXT, NOT NULL)
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

[Додайте інші таблиці, якщо реалізовано]
```


## Опис реалізованої функціональності

#### Система відгуків

Реалізовано сторінку `/feedback`, яка містить HTML-форму. Дані з форми зберігаються в таблицю `feedback`.

#### Магазин

Реалізовано головну сторінку (`/`), яка відображає всі товари. У навігації додано випадаюче меню, яке динамічно формується з таблиці `categories` і дозволяє фільтрувати товари, переходячи на `/category/<id>`.

#### Адміністративна панель

Адмін-панель розділена на два розділи:
1.  **Відгуки (`/admin`):** Дозволяє переглядати та видаляти відгуки.
2.  **Категорії (`/admin/categories`):** Дозволяє переглядати, додавати нові та видаляти існуючі категорії.

#### Додаткова функціональність (Рівень 3)

1.  **Пошук:** В навігацію додана форма пошуку. Вона відправляє `GET`-запит на `/search?q=...`. Маршрут `routes/shop.py` виконує `SELECT ... WHERE name LIKE ?` запит до БД і показує результати, використовуючи той самий шаблон `home.html`.
2.  **Кошик:** На картках товару є кнопка "Купити", яка методом `POST` додає `sneaker_id` у `session['cart']`. У `base.html` відображається кількість товарів у кошику. Сторінка `/cart` (`templates/cart.html`) показує детальний вміст кошика, загальну суму та кнопку "Очистити кошик".

## Ключові фрагменти коду

### Ініціалізація бази даних

Оновлений `models.py` зі створенням трьох таблиць та зовнішнього ключа (FOREIGN KEY):

```python
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
```

### CRUD операції

Наведіть приклади реалізації CRUD операцій:

#### Створення (Create)

```python
@admin_bp.route('/admin/categories', methods=['GET', 'POST'])
def manage_categories():
    conn = get_db_conn()
    if request.method == 'POST':
        if request.form['action'] == 'add':
            category_name = request.form['name']
            if category_name:
                try:
                    conn.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
                    conn.commit()
                except conn.IntegrityError:
                    pass 
        return redirect(url_for('admin.manage_categories'))
    
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()
    return render_template('admin_categories.html', categories=categories)
```

#### Читання (Read)

```python
@shop_bp.route('/search')
def search():
    query = request.args.get('q', '') 
    conn = get_db_conn()
    search_results = conn.execute('''
        SELECT s.*, c.name as category_name 
        FROM sneakers s
        LEFT JOIN categories c ON s.category_id = c.id
        WHERE s.name LIKE ? OR s.description LIKE ?
    ''', (f'%{query}%', f'%{query}%')).fetchall()
    conn.close()
    return render_template('home.html', sneakers=search_results, search_query=query)
```

#### Оновлення (Update)

```python
def update_order_status(order_id, status):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE orders SET status = ? WHERE id = ?',
        (status, order_id)
    )
    conn.commit()
    conn.close()
```

#### Видалення (Delete)

```python
@admin_bp.route('/admin/delete_feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    conn = get_db_conn()
    conn.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.admin_dashboard'))
```

### Маршрутизація

Наведіть приклади маршрутів для роботи з базою даних:

```python
from flask import session, redirect, url_for, request

@shop_bp.route('/cart/add/<int:sneaker_id>', methods=['POST'])
def add_to_cart(sneaker_id):
    # 'session' - це словник, який зберігається для кожного користувача
    cart = session.get('cart', {})
    
    cart_id = str(sneaker_id) 
    cart[cart_id] = cart.get(cart_id, 0) + 1
    
    # Зберігаємо кошик назад у сесію
    session['cart'] = cart
    
    return redirect(request.referrer or url_for('shop.home'))
```

### Робота зі зв'язками між таблицями

Наведіть приклад запиту з використанням JOIN для отримання пов'язаних даних:

```python
# ... (у маршруті @shop_bp.route('/'))
    sneakers_rows = conn.execute('''
        SELECT s.*, c.name as category_name 
        FROM sneakers s
        LEFT JOIN categories c ON s.category_id = c.id
    ''').fetchall()
```

## Розподіл обов'язків у команді

Опишіть внесок кожного учасника команди:

Розподіл обов'язків у команді
-Гринишин Микола: Проєктування та реалізація схеми БД (models.py), включаючи зв'язки (FOREIGN KEY) між sneakers та categories.

-Бугайчук Дмитро: Верстка всіх HTML-шаблонів (base.html, home.html, about.html, feedback.html, admin.html, admin_categories.html, cart.html), налаштування стилів Tailwind CSS, інтеграція Jinja2-циклів у шаблони.

-Гапяк Марк: Реалізація повного циклу адмін-панелі (routes/admin.py): CRUD для відгуків та CRUD для категорій.

-Сюйва Дмитро: Реалізація основної логіки магазину (routes/shop.py): фільтрація за категоріями, пошук, кошик (на базі сесій). Створення скрипту seed.py для наповнення БД.

## Скріншоти

Додайте скріншоти основних функцій вашого вебзастосунку:

### Форма зворотного зв'язку
![alt text](image-3.png)

![Форма зворотного зв'язку](шлях/до/скріншоту)

### Каталог товарів

![Каталог товарів](шлях/до/скріншоту)
![alt text](image-1.png)

### Адміністративна панель
![alt text](image-2.png)
![Адмін-панель](шлях/до/скріншоту)

### Управління замовленнями
![alt text](image-4.png)
![Управління замовленнями](шлях/до/скріншоту)

### Додаткова функціональність

![Додаткова функція](шлях/до/скріншоту)

## Тестування

### Сценарії тестування

Опишіть, які сценарії ви тестували:

Сценарії тестування:
1  Відгуки: Додавання відгуку -> Перевірка в /admin -> Видалення відгуку -> Перевірка, що він зник.

2 Категорії: Додавання категорії "Тест" в /admin/categories -> Перевірка, що вона з'явилась у списку та в меню на сайті -> Видалення категорії.

3 Товари: Запуск seed.py -> Перевірка, що товари з'явились на головній та мають правильні категорії.

4 Фільтрація: Клік на категорію "Лайфстайл" -> Перевірка, що на сторінці лише "Nike Air Force 1" та "Adidas Superstar".

5 Пошук: Введення "Nike" у пошук -> Перевірка, що у результатах є "Nike Air Force 1" та "Nike Pegasus 40".

6 Кошик: Натискання "Купити" на 2-х товарах -> Перевірка, що іконка кошика показує "(2)" -> Перехід в /cart, перевірка загальної суми -> Натискання "Очистити кошик".


## Висновки

Опишіть:

-Що вдалося реалізувати: Вдалося успішно реалізувати всі три рівні завдання. Створено повноцінний веб-додаток на Flask, що використовує "чистий" sqlite3, з розділеною логікою, зв'язаними таблицями (товари та категорії) та просунутою логікою (кошик на сесіях, пошук).

-Отримані навички: Отримали глибокі навички роботи з sqlite3, написання складних SQL-запитів (JOIN, LIKE), проектування реляційних баз даних (FOREIGN KEY), та використання сесій у Flask для зберігання стану користувача.

-Труднощі: Найбільші труднощі виникли при оновленні бази даних (необхідність видаляти db.sqlite при зміні схеми) та при передачі даних між різними маршрутами (вирішено за допомогою session для кошика та g для категорій у меню).

-Командна робота: Завдяки чіткій архітектурі (Blueprints) команда могла паралельно працювати над різними частинами функціоналу (один над адмінкою, інший над кошиком), не заважаючи один одному.

-Покращення: У майбутньому варто додати автентифікацію для /admin (щоб захистити її паролем) та реалізувати таблицю Orders для збереження замовлень з кошика в БД.

Очікувана оцінка: [8-12 балів]

Обґрунтування: [ми старались]
