import re


class ValidationError(Exception):
    def __init__(self, message: str, field: str):
        super().__init__({"error": message, "field": field})


class Validate:
    def email_valid(email: str) -> bool:
        """
        Checks if email is valid
        """
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return re.fullmatch(regex, email) != None

    def password_valid(password: str):
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,20}$"
        return bool(re.search(regex, password))

    def validate_email(email: str):
        """
        Validates email according to required regex pattern and raises a ValidationError if email does not match
        """
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        is_valid = re.fullmatch(regex, email) != None
        if not is_valid:

            raise ValidationError(
                "Invalid email -> Please enter a valid email", "email"
            )

    def validate_password(password: str):
        """
        Validates password according to required regex pattern and raises a ValidationError if password does not match
        """
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@!#$%^&*()-.,])[A-Za-z\d@!#$%^&*()-.,]{6,20}$"
        if not (re.search(regex, password) != None):

            raise ValidationError(
                f"Invalid password -> "
                + "Password must at least 6 characters long and contain at least one uppercase letter, lowercase letter, number and special character",
                "password",
            )
