from django.contrib.sitemaps.views import sitemap
from django.urls import path

from .sitemaps import get_sitemaps
from .views import favicon, home

urlpatterns = [
    # Sitemaps
    path("sitemap.xml", sitemap, {"sitemaps": get_sitemaps()}, name="django.contrib.sitemaps.views.sitemap"),
    # Favicon
    path("favicon.ico", favicon, name="favicon"),
    # Home
    path("", home, name="home"),
]
