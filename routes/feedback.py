from flask import Blueprint, render_template, request, redirect, url_for
from models import get_db_conn

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def handle_feedback():
    
    if request.method == 'POST':
        
        user_name = request.form['user_name']
        email = request.form['email']
        message = request.form['message']
        
        
        conn = get_db_conn()
        conn.execute(
            'INSERT INTO feedback (user_name, email, message) VALUES (?, ?, ?)',
            (user_name, email, message)
        )
        conn.commit()
        conn.close()
        
        
        return redirect(url_for('shop.home'))

    
    
    return render_template('feedback.html')