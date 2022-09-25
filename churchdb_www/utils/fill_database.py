import random
import string
import os

import sys
sys.path.append("/home/imagine/Documents/ChurchDB/")

from churchdb_www.models import *
from churchdb_www import create_app

def gen_rand_fc() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


def gen_rand_bd() -> str:
    year = random.randint(1900, 2020)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month}-{day}"


def gen_rand_pn() -> str:
    return f"+{random.randint(100000000000, 999999999999)}"


def get_emails(first_names: list[str], last_names: list[str]) -> list[str]:
    DOMAINS = [
        "napoli.rolex",
        "pizza.mrg",
        "carbo.nara",
        "rabbit.hole",
        "fuck.java",
        "assembl.er",
        "bread.board",
        "nuker.boom",
        "fort.nait",
        "la.pubg"
    ]

    emails = []

    for first_name, last_name in zip(first_names, last_names):
        emails.append(f"{first_name.lower()}.{last_name.lower()}@{random.choice(DOMAINS)}")

    return emails


if __name__ == "__main__":
    create_app().app_context().push()

    db.drop_all()
    db.create_all()

    random.seed(os.urandom(16))

    FIRST_NAMES = [
        "Alfredo",
        "Marco",
        "Giovanni",
        "Giorgio",
        "Gianni",
        "Maurizio",
        "Giacomo",
        "Ciro",
        "Rosario",
        "Jessica"
    ]

    LAST_NAMES = [
        "Esposito",
        "Bianchi",
        "Rossi",
        "Bruno",
        "Giordano",
        "Ronaldo",
        "Pirlo",
        "White",
        "Pinkman",
        "Jiniux"
    ]

    random.shuffle(FIRST_NAMES)
    random.shuffle(LAST_NAMES)

    EMAILS = get_emails(FIRST_NAMES, LAST_NAMES)

    PERSONS = []

    for first_name, last_name, email in zip(FIRST_NAMES, LAST_NAMES, EMAILS):
        person = Person(
            first_name,
            last_name,
            gen_rand_fc(),
            gen_rand_bd(),
            email,
            gen_rand_pn()
        )

        PERSONS.append(person)

        certificates = [
            BaptismalCertificate(),
            FirstCommunionCertificate(),
            ConfirmationCertificate(),
            DeathCertificate()
        ]

        for certificate in certificates:
            certificate.released_to_person = person

        db.session.add(person)
        db.session.add_all(certificates)

    COUPLES = list(range(len(FIRST_NAMES)))
    random.shuffle(COUPLES)

    for p1, p2 in zip(COUPLES[::2], COUPLES[1::2]):
        marriage = MarriageCertificate()
        marriage.released_to_person_1 = PERSONS[p1]
        marriage.released_to_person_2 = PERSONS[p2]

        db.session.add(marriage)

    db.session.add(User('paperino', 'quackquack', True))
    db.session.add(User('pippo', 'ferrarif40', False))

    db.session.commit()
