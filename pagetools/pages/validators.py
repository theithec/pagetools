from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


def validate_emails_str(emails: str):

    validate = EmailValidator()
    for email in emails.split(","):
        if not email:
            continue
        validate(email)
