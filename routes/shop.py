from flask import (
    Blueprint, render_template, g, request, 
    session, redirect, url_for
)
from models import get_db_conn

shop_bp = Blueprint('shop', __name__)


@shop_bp.before_request
def load_categories():
    conn = get_db_conn()
    g.categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()



@shop_bp.route('/')
def home():
    conn = get_db_conn()
    sneakers_rows = conn.execute('''
        SELECT s.*, c.name as category_name 
        FROM sneakers s
        LEFT JOIN categories c ON s.category_id = c.id
    ''').fetchall()
    conn.close()
    return render_template('home.html', sneakers=sneakers_rows)

@shop_bp.route('/about')
def about():
    return render_template('about.html')

@shop_bp.route('/category/<int:category_id>')
def category_view(category_id):
    conn = get_db_conn()
    sneakers_rows = conn.execute('''
        SELECT s.*, c.name as category_name 
        FROM sneakers s
        JOIN categories c ON s.category_id = c.id
        WHERE s.category_id = ?
    ''', (category_id,)).fetchall()
    
    category_name = conn.execute('SELECT name FROM categories WHERE id = ?', (category_id,)).fetchone()['name']
    conn.close()
    
    return render_template('home.html', sneakers=sneakers_rows, category_name=category_name)



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



@shop_bp.route('/cart/add/<int:sneaker_id>', methods=['POST'])
def add_to_cart(sneaker_id):
    cart = session.get('cart', {})
    
    cart_id = str(sneaker_id) 
    cart[cart_id] = cart.get(cart_id, 0) + 1
    
    session['cart'] = cart
    
    
    return redirect(request.referrer or url_for('shop.home'))

@shop_bp.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    if not cart:
        return render_template('cart.html', items=[], total_price=0)

    conn = get_db_conn()
    
    item_ids = list(cart.keys())
    placeholders = ','.join('?' for id in item_ids)
    
    query = f'SELECT * FROM sneakers WHERE id IN ({placeholders})'
    db_items = conn.execute(query, item_ids).fetchall()
    
    items_in_cart = []
    total_price = 0
    
    for item in db_items:
        item_id_str = str(item['id'])
        quantity = cart[item_id_str]
        item_total = item['price'] * quantity
        
        items_in_cart.append({
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'image_url': item['image_url'],
            'quantity': quantity,
            'total': item_total
        })
        total_price += item_total
        
    conn.close()
    
    return render_template('cart.html', items=items_in_cart, total_price=total_price)

@shop_bp.route('/cart/clear')
def clear_cart():
    session['cart'] = {}
    return redirect(url_for('shop.view_cart'))