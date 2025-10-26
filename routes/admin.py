from flask import Blueprint, render_template, request, redirect, url_for
from models import get_db_conn

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