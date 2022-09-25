from email.utils import parseaddr
import codicefiscale
import datetime
import phonenumbers

def validate_name(name: str) -> bool:
    return name.replace(" ", "").isalpha() or not name

def validate_email(email: str) -> bool:
    checker = [ "@", "." ]
    
    return all(char in parseaddr(email)[1] for char in checker) or not email

def validate_fiscal_code(fiscal_code: str) -> bool:
    return codicefiscale.isvalid(fiscal_code) or not fiscal_code

def validate_birth_date(birth_date: str) -> bool:
    if not birth_date:
        return True

    year, month, day = birth_date.split("-")
    try:
        datetime.datetime(int(year), int(month), int(day))
        return True
    except ValueError:
        return False

def validate_phone_number(phone_number: str) -> bool:
    if not phone_number:
        return True
        
    return phonenumbers.is_valid_number(phonenumbers.parse(phone_number))

def validate_search_option(search_option: str) -> bool:
    return search_option in ["persons", "certificates"]

def validate_all(first_name: str = "", last_name: str = "", fiscal_code: str = "", birth_date: str = "", email: str = "", phone: str = "", search_option: str = "") -> bool:
    STATUSES = [True] * 7
    STATUSES[0] = validate_name(first_name)
    STATUSES[1] = validate_name(last_name)
    STATUSES[2] = validate_fiscal_code(fiscal_code)
    STATUSES[3] = validate_birth_date(birth_date)
    STATUSES[4] = validate_email(email)
    STATUSES[5] = validate_phone_number(phone)
    STATUSES[6] = validate_search_option(search_option)

    for i, v in enumerate(STATUSES):
        if not v:
            print(f"{i} FAILED")

    return all(STATUSES)