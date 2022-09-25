from flask import Flask, render_template
from flask_login import LoginManager

from churchdb_www.models import db, User

from churchdb_www.main.routes import main
from churchdb_www.search.routes import search
from churchdb_www.create.routes import create
from churchdb_www.view.routes import view

def bad_request(e):
    return render_template('error.html', error_code="400", error_msg="Bad request!"), 400

def unauthorized(e):
    return render_template('error.html', error_code="401", error_msg="No permissions!"), 401

def page_not_found(e):
    return render_template('error.html', error_code="404", error_msg="Page not found!"), 404

def method_not_allowed(e):
    return render_template('error.html', error_code="405", error_msg="Method not allowed!"), 405

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(search, url_prefix='/search')
    app.register_blueprint(create, url_prefix='/create')
    app.register_blueprint(view, url_prefix='/view')
    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
        
    return app