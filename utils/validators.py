import re

from django.contrib.auth.password_validation import validate_password


valid_email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def is_valid_email(email: str):
    return re.fullmatch(valid_email_regex, email)


    
# def is_valid_password(password: str) -> list[bool, list[str]]:
def is_valid_password(password: str):
    try:
        validate_password(password)
        return True, []

    except Exception as response:
        return False, response
