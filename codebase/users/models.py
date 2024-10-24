from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.functional import cached_property


class User(AbstractUser):
    asked_to_verify_email = models.BooleanField(default=False)
    country_code = models.CharField(max_length=8, null=True)
    whatsapp_number = models.CharField(max_length=16, default="")

    @cached_property
    def cleaned_whatsapp_number(self):
        return self.whatsapp_number.replace(" ", "")

    @cached_property
    def total_cost_in_books(self) -> Decimal:
        try:
            return self.bookinstance_set.all().aggregate(Sum("book__price"))["book__price__sum"]
        except Exception:  # TODO: besser machen!
            return Decimal(0.0)

    @cached_property
    def delete_account_url(self):
        return reverse("user-delete", kwargs={"id": self.id})

    def __str__(self) -> str:
        return f"{self.username} | {self.email}"
