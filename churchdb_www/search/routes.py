from flask import Blueprint, render_template, request, abort
from flask_login import login_required
from flask_sqlalchemy import *

from churchdb_www.models import Person, BaptismalCertificate, FirstCommunionCertificate, ConfirmationCertificate, MarriageCertificate, DeathCertificate

import churchdb_www.utils.validate_input as validate_input

search = Blueprint('search', __name__)


@search.route('/')
@login_required
def index():
    return render_template('search.html')


def filter_persons(first_name=None, last_name=None, fiscal_code=None, birth_date=None, email=None, phone=None):
    persons = Person.query

    if first_name:
        persons = persons.filter_by(first_name=first_name)
    if last_name:
        persons = persons.filter_by(last_name=last_name)
    if fiscal_code:
        persons = persons.filter_by(fiscal_code=fiscal_code)
    if birth_date:
        persons = persons.filter_by(date_of_birth=birth_date)
    if email:
        persons = persons.filter_by(email=email)
    if phone:
        persons = persons.filter_by(phone=phone)

    return persons


def get_baptismal_certificates(ids: list):
    return BaptismalCertificate.query.filter(
        BaptismalCertificate.released_to_id.in_(ids)).all()


def get_first_communion_certificates(ids: list):
    return FirstCommunionCertificate.query.filter(
        FirstCommunionCertificate.released_to_id.in_(ids)).all()


def get_confirmation_certificates(ids: list):
    return ConfirmationCertificate.query.filter(
        ConfirmationCertificate.released_to_id.in_(ids)).all()


def get_marriage_certificates(ids: list):
    return MarriageCertificate.query.filter(MarriageCertificate.released_to_id_1.in_(
        ids) | MarriageCertificate.released_to_id_2.in_(ids)).all()


def get_death_certificates(ids: list):
    return DeathCertificate.query.filter(
        DeathCertificate.released_to_id.in_(ids)).all()


@search.route('/get_results', methods=['POST'])
@login_required
def get_results():
    first_name = request.form.get('first_name', "", type=str)
    last_name = request.form.get('last_name', "", type=str)
    fiscal_code = request.form.get('fiscal_code', "", type=str)
    birth_date = request.form.get('birth_date', "", type=str)
    email_address = request.form.get('email_address', "", type=str)
    phone_number = request.form.get('phone_number', "", type=str)
    search_option = request.form.get('search_option', "", type=str)

    if not validate_input.validate_all(first_name, last_name, fiscal_code, birth_date, email_address, phone_number, search_option):
        abort(400)

    if search_option == 'certificates':
        ids = [person.id for person in filter_persons(
            first_name, last_name, fiscal_code, birth_date, email_address, phone_number)]

        results = []
        results += get_baptismal_certificates(ids)
        results += get_first_communion_certificates(ids)
        results += get_confirmation_certificates(ids)
        results += get_marriage_certificates(ids)
        results += get_death_certificates(ids)
    else:
        results = [person for person in filter_persons(
            first_name, last_name, fiscal_code, birth_date, email_address, phone_number)]

    return {"results": results}
