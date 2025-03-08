"""Blog Views."""

from django.views.generic import ListView, DetailView
from django.utils.functional import cached_property
from django.urls import reverse

from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin

from .models import Post


class PostListView(ListBreadcrumbMixin, ListView):
    """Displays a list of posts."""

    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    ordering = "-created"


class PostDetailView(DetailBreadcrumbMixin, DetailView):
    """Displays a single post."""

    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
