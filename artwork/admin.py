"""Artwork admin."""

from django.contrib import admin
from .models import Artist, Artwork


@admin.register(Artist)
class Artist(admin.ModelAdmin):
    """Artist admin."""

    list_display = (
        "__str__",
        "name",
        "country",
    )


@admin.register(Artwork)
class Artwork(admin.ModelAdmin):
    """Artwork admin."""

    list_display = (
        "__str__",
        "title",
        "artist",
        "image",
    )
    list_filter = ("artist",)
