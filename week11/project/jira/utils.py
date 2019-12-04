import os
from django.core.exceptions import ValidationError

ALLOWED_EXTS = ['.pdf', '.doc', '.docx']


def validate_file_size(value):
    if value.size > 1000000:
        raise ValidationError('max file size: 1Mb')


def validate_extension(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in ALLOWED_EXTS:
        raise ValidationError('not allowed file ext, allowed: {ALLOWED_EXTS}')
