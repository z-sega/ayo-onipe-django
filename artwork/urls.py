"""Blog urls."""

from django.urls import path
from .views import ArtworkListView, ArtworkDetailView

app_name = "artwork"

urlpatterns = [
    path("art/", ArtworkListView.as_view(), name="artwork_list"),
    path("art/<int:pk>/", ArtworkDetailView.as_view(), name="artwork_detail"),
]
