"""Core urls."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("me/", views.MeView.as_view(), name="me"),
    path("site-map/", views.SiteMapView.as_view(), name="site_map"),
]
