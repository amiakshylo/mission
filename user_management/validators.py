import os

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def validate_profile_image(file):
    max_size_mb = 5 * 1024 * 1024

    if file.size > max_size_mb:
        raise ValidationError("Image can't be larger than 5 MB!")

    width, height = get_image_dimensions(file)
    max_width, max_height = 2000, 2000
    if width > max_width or height > max_height:
        raise ValidationError(f"Image dimensions should not exceed {max_width}x{max_height} pixels.")

    file_extension = os.path.splitext(file.title)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if file_extension not in valid_extensions:
        raise ValidationError("Unsupported file extension. Allowed extensions are: '.jpg', '.jpeg', '.png'.")
