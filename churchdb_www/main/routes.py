from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_user
from werkzeug.security import check_password_hash
from churchdb_www.models import User

main = Blueprint('main', __name__)

def check_credentials(username: str, password: str) -> bool:
    """Check if the given credentials are correct.

    Args:
        username (str): username
        password (str): password

    Returns:
        bool: True if the credentials are correct, False otherwise
    """
    
    user = User.query.filter_by(username=username).first()
    if user:
        return check_password_hash(user.password, password)

    return False


@main.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if check_credentials(username, password):
            user = User.query.filter_by(username=username).first()
            login_user(user)

            return redirect(url_for('search.index'))
        else:
            flash('Invalid username or password')

    return render_template('main.html', no_navbar=True)

@main.route('/test_abort')
def test():
    abort(400)
    return "This will never be executed"