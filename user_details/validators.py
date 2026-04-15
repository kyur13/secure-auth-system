import re
from django.core.exceptions import ValidationError

def validate_gmail(email):
    if not email.endswith('@gmail.com'):
        raise ValidationError("Email must be a @gmail.com address")

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")

    if not re.search(r'\d', password):
        raise ValidationError("Password must contain a number")

    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        raise ValidationError("Password must contain a special character")