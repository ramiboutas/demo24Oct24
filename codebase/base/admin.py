from django.contrib import admin

from .models import MenuItem, PageLink


class PageLinkInline(admin.TabularInline):
    model = PageLink
    extra = 3


@admin.register(MenuItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ("title", "show_in_navbar", "show_in_footer")
    list_filter = ("show_in_navbar", "show_in_footer")
    inlines = (PageLinkInline,)


from django.contrib.sessions.models import Session

admin.site.register(Session)
