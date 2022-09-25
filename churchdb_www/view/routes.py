from flask import Blueprint
from flask_login import login_required

from churchdb_www.models import Person

view = Blueprint('view', __name__)

@login_required
@view.route('/person/<int:id>')
def person(id):
    person = Person.query.get(id)
    person_info = f"""
    ID: {person.id}<br />
    First Name: {person.first_name}<br />
    Last Name: {person.last_name}<br />
    Fiscal Code: {person.fiscal_code}<br />
    Birth Date: {person.birth_date}<br />
    Email: {person.email}<br />
    Phone: {person.phone}
    """
    return person_info