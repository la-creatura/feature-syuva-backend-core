from flask import Flask

from models import init_db


from routes.shop import shop_bp
from routes.admin import admin_bp
from routes.feedback import feedback_bp


init_db()


app = Flask(__name__)


app.config['SECRET_KEY'] = 'your-very-secret-random-key-12345' 


app.register_blueprint(shop_bp) 
app.register_blueprint(admin_bp, url_prefix='/admin') 
app.register_blueprint(feedback_bp) 


if __name__ == '__main__':
    app.run(debug=True)

    
from flask import request, redirect, render_template
from models import add_sneaker, get_all_sneakers, delete_sneaker, get_categories

@app.route('/admin/manage_catalog', methods=['GET', 'POST'])
def manage_catalog():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        category_id = request.form.get('category_id') or None
        
        add_sneaker(name, description, price, image_url, category_id)
        return redirect(request.referrer or '/admin/manage_catalog')
    
    sneakers = get_all_sneakers()
    categories = get_categories()
    return render_template('admin_catalog.html', sneakers=sneakers, categories=categories)

@app.route('/admin/delete_sneaker/<int:sneaker_id>', methods=['POST'])
def delete_sneaker_route(sneaker_id):
    delete_sneaker(sneaker_id)
    return redirect(request.referrer or '/admin/manage_catalog')    