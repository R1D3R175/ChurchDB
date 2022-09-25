from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from dataclasses import dataclass

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model

    Constructor:
        username (str): username
        password (str): password (will be hashed)
        is_admin (bool): is admin?
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(102), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return f"<Admin: {self.username}>" if self.is_admin else f"<User: {self.username}>"

@dataclass
class Person(db.Model):
    """Generic person model

    Constructor:
        first_name (str): first name of the person
        last_name (str): last name of the person
        date_of_birth (str): date of birth of the person (YYYY-MM-DD)
        fiscal_code (str): fiscal code of the person
        email (str): email of the person
        phone (str): phone of the person
    """

    id: int
    first_name: str
    last_name: str
    fiscal_code: str
    birth_date: str
    email: str
    phone: str
    type: str = "person"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    fiscal_code = db.Column(db.String(16), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(13), nullable=True)

    def __init__(self, first_name: str, last_name: str, fiscal_code: str, birth_date: str = "", email: str = "", phone: str = ""):
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
        self.fiscal_code = fiscal_code
        self.birth_date = birth_date
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f"<Person: {self.first_name} {self.last_name}>"

@dataclass
class BaptismalCertificate(db.Model):

    id: int
    released_to_id: int
    released_to_person: Person
    type: str = "baptismal"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    released_to_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    released_to_person = db.relationship('Person', foreign_keys=[released_to_id])


    # TODO: FILL DATA

@dataclass
class FirstCommunionCertificate(db.Model):

    id: int
    released_to_id: int
    released_to_person: Person
    type: str = "first_communion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    released_to_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    released_to_person = db.relationship('Person', foreign_keys=[released_to_id])

    # TODO: FILL DATA

@dataclass
class ConfirmationCertificate(db.Model):

    id: int
    released_to_id: int
    released_to_person: Person
    type: str = "confirmation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    released_to_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    released_to_person = db.relationship('Person', foreign_keys=[released_to_id])

    # TODO: FILL DATA

@dataclass
class MarriageCertificate(db.Model):

    id: int
    released_to_id_1: int
    released_to_id_2: int
    released_to_person_1: Person
    released_to_person_2: Person
    type: str = "marriage"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    released_to_id_1 = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    released_to_id_2 = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    released_to_person_1 = db.relationship('Person', foreign_keys=[released_to_id_1])
    released_to_person_2 = db.relationship('Person', foreign_keys=[released_to_id_2])

    # TODO: FILL DATA

@dataclass
class DeathCertificate(db.Model):

    id: int
    released_to_id: int
    released_to_person: Person
    type: str = "death"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    released_to_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    released_to_person = db.relationship('Person', foreign_keys=[released_to_id])

    # TODO: FILL DATA