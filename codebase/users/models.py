from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class User(AbstractUser):
    asked_to_verify_email = models.BooleanField(default=False)
    country_code = models.CharField(max_length=8, null=True)

    @cached_property
    def delete_account_url(self):
        return reverse("user-delete", kwargs={"id": self.id})

    def __str__(self) -> str:
        return f"{self.username} | {self.email}"
