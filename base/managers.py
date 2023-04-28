from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password, first_name, last_name, account_balance, currency, **other_fields):

        username = self.normalize_email(username)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, account_balance=account_balance,
                          currency=currency, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if other_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user
