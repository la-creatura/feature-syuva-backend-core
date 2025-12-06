from flask import Flask

from models import init_db


from routes.shop import shop_bp
from routes.admin import admin_bp
from routes.feedback import feedback_bp


init_db()


app = Flask(__name__, static_folder='static', static_url_path='/static')


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

import os
from werkzeug.utils import secure_filename
from flask import url_for

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return {'error': 'Немає файлу'}, 400
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return {'error': 'Невірний формат'}, 400
    
    filename = secure_filename(file.filename)
    # додайте унікальний префікс до назви
    import uuid
    filename = f"{uuid.uuid4()}_{filename}"
    
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    return {'url': url_for('static', filename=f'uploads/{filename}')}