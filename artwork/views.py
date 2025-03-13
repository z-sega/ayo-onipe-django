"""Artwork Views."""

from django.views.generic import ListView, DetailView
from django.utils.functional import cached_property
from django.urls import reverse

from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin

from .models import Artwork


class ArtworkListView(ListBreadcrumbMixin, ListView):
    """Displays a list of posts."""

    model = Artwork
    template_name = "artwork_list.html"
    context_object_name = "artworks"
    ordering = "title"


class ArtworkDetailView(DetailBreadcrumbMixin, DetailView):
    """Displays a single post."""

    model = Artwork
    template_name = "artwork_detail.html"
    context_object_name = "artwork"
