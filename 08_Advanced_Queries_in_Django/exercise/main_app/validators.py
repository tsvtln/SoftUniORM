from django.core.exceptions import ValidationError


class RangeValueValidator:
    def __init__(self, min_value: int, max_value: int, message=None):
        self.min_value = min_value
        self.max_value = max_value
        if not message:
            self.message = f"The rating must be between {self.min_value:.1f} and {self.max_value:.1f}"
        else:
            self.message = message

    def __call__(self, value: int):
        if not self.min_value <= value <= self.max_value:
            raise ValidationError(self.message)

    def deconstruct(self):
        return (
            'main_app.validators.RangeValueValidator',
            [self.min_value, self.max_value],
            {'message': self.message}
        )
