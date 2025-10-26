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