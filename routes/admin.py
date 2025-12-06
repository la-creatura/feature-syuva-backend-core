from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import get_db_conn
import os
import uuid
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__)




@admin_bp.route('/')
def admin_dashboard():
    conn = get_db_conn()
    feedbacks = conn.execute('SELECT * FROM feedback ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin.html', feedbacks=feedbacks)


@admin_bp.route('/delete_feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    conn = get_db_conn()
    conn.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.admin_dashboard'))



@admin_bp.route('/categories', methods=['GET', 'POST'])
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


@admin_bp.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    conn = get_db_conn()
    try:
        conn.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
    except conn.IntegrityError:
        pass
    conn.close()
    return redirect(url_for('admin.manage_categories'))


@admin_bp.route('/catalog', methods=['GET', 'POST'])
def manage_catalog():
    conn = get_db_conn()

    if request.method == 'POST':
        # add new sneaker
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        category_id = request.form.get('category_id') or None

        if name and price:
            try:
                conn.execute('''
                    INSERT INTO sneakers (name, description, price, image_url, category_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, description, int(price), image_url, category_id))
                conn.commit()
            except Exception:
                pass

        return redirect(url_for('admin.manage_catalog'))

    sneakers = conn.execute('''
        SELECT s.*, c.name as category_name
        FROM sneakers s
        LEFT JOIN categories c ON s.category_id = c.id
        ORDER BY s.id DESC
    ''').fetchall()

    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()
    return render_template('admin_catalog.html', sneakers=sneakers, categories=categories)


@admin_bp.route('/delete_sneaker/<int:sneaker_id>', methods=['POST'])
def delete_sneaker(sneaker_id):
    conn = get_db_conn()
    try:
        conn.execute('DELETE FROM sneakers WHERE id = ?', (sneaker_id,))
        conn.commit()
    except Exception:
        pass
    conn.close()
    return redirect(url_for('admin.manage_catalog'))


@admin_bp.route('/catalog/edit/<int:sneaker_id>', methods=['GET', 'POST'])
def edit_sneaker(sneaker_id):
    conn = get_db_conn()
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        category_id = request.form.get('category_id') or None

        try:
            conn.execute('''
                UPDATE sneakers
                SET name = ?, description = ?, price = ?, image_url = ?, category_id = ?
                WHERE id = ?
            ''', (name, description, int(price) if price else None, image_url, category_id, sneaker_id))
            conn.commit()
        except Exception:
            pass
        conn.close()
        return redirect(url_for('admin.manage_catalog'))

    sneaker = conn.execute('SELECT * FROM sneakers WHERE id = ?', (sneaker_id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()
    if not sneaker:
        return redirect(url_for('admin.manage_catalog'))
    return render_template('admin_catalog_edit.html', sneaker=sneaker, categories=categories)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_bp.route('/upload_image', methods=['POST'])
def upload_image():
    # Accepts a file from form field 'file' and stores it under static/uploads
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    # Compute uploads directory relative to project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    uploads_dir = os.path.join(project_root, 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    save_path = os.path.join(uploads_dir, unique_name)
    try:
        file.save(save_path)
    except Exception as e:
        return jsonify({'error': 'Failed to save file'}), 500

    file_url = url_for('static', filename=f'uploads/{unique_name}')
    return jsonify({'url': file_url}), 200