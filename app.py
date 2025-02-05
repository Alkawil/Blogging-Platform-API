from flask import Flask
from models import db, BlogPost
from routes import blog_routes
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(blog_routes)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
