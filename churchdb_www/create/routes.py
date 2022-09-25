from flask import Blueprint, render_template, url_for, request, abort
from flask_login import login_required, current_user

from churchdb_www.models import db, Person

import churchdb_www.utils.validate_input as validate_input

create = Blueprint('create', __name__)

@create.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.is_admin:
        abort(401)

    if request.method == 'POST':
        first_name = request.form.get('first_name', "", type=str)
        last_name = request.form.get('last_name', "", type=str)
        fiscal_code = request.form.get('fiscal_code', "", type=str)
        birth_date = request.form.get('birth_date', "", type=str)
        email_address = request.form.get('email_address', "", type=str)
        phone_number = request.form.get('phone_number', "", type=str)

        if not validate_input.validate_all(first_name, last_name, fiscal_code, birth_date, email_address, phone_number):
            abort(400)

        person = Person(first_name=first_name, last_name=last_name, fiscal_code=fiscal_code, date_of_birth=birth_date, email_address=email_address, phone_number=phone_number)
        db.session.add(person)
        db.session.commit()

    return render_template('create.html')