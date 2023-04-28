from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# currency choices user can select
CURRENCY_CHOICES = [
    ('gbp', 'GBP'),
    ('usd', 'USD'),
    ('eur', 'EURO'),
]


class CustomUser(AbstractUser):

    account_balance = models.DecimalField(max_digits=20, decimal_places=2, default=1000, blank=True)
    currency = models.CharField(max_length=4, choices=CURRENCY_CHOICES, blank=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
