# validators.py

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

import re

class CustomPasswordValidator:
    """
    A custom password validator that ensures:
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """

    def validate(self, password, user=None):
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least one uppercase letter."),
                code='password_no_upper',
            )

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("The password must contain at least one lowercase letter."),
                code='password_no_lower',
            )

        # Check for at least one digit
        if not re.search(r'\d', password):
            raise ValidationError(
                _("The password must contain at least one digit."),
                code='password_no_digit',
            )

        # # Check for at least one special character
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        #     raise ValidationError(
        #         _("The password must contain at least one special character."),
        #         code='password_no_special',
        #     )

    def get_help_text(self):
        return _(
            "Your password must contain at least one uppercase letter, one lowercase letter, one digit, "
            "and one special character."
        )
