# Generated by Django 4.1.7 on 2023-04-24 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_email', models.CharField(max_length=256)),
                ('receiver_email', models.CharField(max_length=256)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('converted_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sender_prev_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sender_new_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receiver_prev_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receiver_new_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sender_currency_at_time', models.CharField(max_length=4)),
                ('receiver_currency_at_time', models.CharField(max_length=4)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
