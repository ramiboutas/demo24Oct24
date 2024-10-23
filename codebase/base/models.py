from auto_prefetch import ForeignKey, Model
from django.db import models


class MenuItem(Model):
    title = models.CharField(max_length=64)
    order = models.IntegerField(default=0)
    show_in_navbar = models.BooleanField(default=True)
    show_in_footer = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    class Meta(Model.Meta):
        ordering = ("order",)


class PageLink(Model):
    menu_item = ForeignKey(MenuItem, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=True, blank=True)
    url = models.URLField(max_length=128, null=True, blank=True)
    target_blank = models.BooleanField(default=False)

    def __str__(self):
        return self.title
