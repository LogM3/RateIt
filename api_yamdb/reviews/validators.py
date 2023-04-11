from django.core.validators import ValidationError


def score_validator(value):
    if 1 > value or 10 < value:
        raise ValidationError('Убедитесь, что поставили оценку от 1 до 10')
