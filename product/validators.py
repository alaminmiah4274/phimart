from django.core.exceptions import ValidationError


def validate_file_size(file):
    """this validator validates if the file size less than 10 MB"""

    max_size = 30
    max_size_in_bytes = max_size * 1024

    if file.size > max_size_in_bytes:
        raise ValidationError(f"File can not be larger than {max_size} KB")
