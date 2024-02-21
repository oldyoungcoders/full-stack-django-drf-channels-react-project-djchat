import os

from django.core.exceptions import ValidationError
from PIL import Image


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.height > 70 or img.width > 100:
                raise ValidationError(
                    f"The maximum image size is 70x70 pixels. size: {img.height}x{img.width} pixels."
                )


def validate_image_file_extension(image):
    ext = os.path.splitext(image.name)[1]
    valid_extensions = [".png", ".jpg", ".jpeg", ".gif"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension.")
