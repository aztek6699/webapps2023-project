from django.db import models


class Transfer(models.Model):
    sender_email = models.CharField(max_length=256)
    receiver_email = models.CharField(max_length=256)

    amount = models.DecimalField(max_digits=20, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=20, decimal_places=2)

    sender_prev_amount = models.DecimalField(max_digits=20, decimal_places=2)
    sender_new_amount = models.DecimalField(max_digits=20, decimal_places=2)

    receiver_prev_amount = models.DecimalField(max_digits=20, decimal_places=2)
    receiver_new_amount = models.DecimalField(max_digits=20, decimal_places=2)

    sender_currency_at_time = models.CharField(max_length=4)
    receiver_currency_at_time = models.CharField(max_length=4)

    date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        detail = ''
        detail += self.sender_email
        detail += '->'
        detail += self.receiver_email
        return detail
