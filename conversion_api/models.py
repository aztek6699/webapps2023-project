from django.db import models


class ConversionResponse(models.Model):
    amount = models.FloatField()
    message = models.CharField(max_length=256)
    is_success = models.BooleanField(default=False)
    objects = models.Manager()

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, amount, message, is_success, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amount = amount
        self.message = message
        self.is_success = is_success


