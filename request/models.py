from django.db import models


class Request(models.Model):
    patron_email = models.CharField(max_length=256)
    receiver_email = models.CharField(max_length=256)

    amount = models.DecimalField(max_digits=20, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=20, decimal_places=2)

    patron_prev_amount = models.DecimalField(max_digits=20, decimal_places=2, default=None, blank=True, null=True)
    patron_new_amount = models.DecimalField(max_digits=20, decimal_places=2, default=None, blank=True, null=True)
    patron_currency_at_time = models.CharField(max_length=4)

    receiver_prev_amount = models.DecimalField(max_digits=20, decimal_places=2, default=None, blank=True, null=True)
    receiver_new_amount = models.DecimalField(max_digits=20, decimal_places=2, default=None, blank=True, null=True)
    receiver_currency_at_time = models.CharField(max_length=4)

    pending = models.BooleanField()
    accepted = models.BooleanField()

    date_requested = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(default=None, blank=True, null=True)

    objects = models.Manager()
