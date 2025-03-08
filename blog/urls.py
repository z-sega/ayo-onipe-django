"""Blog urls."""

from django.urls import path
from .views import PostListView, PostDetailView

app_name = "blog"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
]
