"""Core views."""

from django.http import HttpResponse


def home(request):
    """Core home view."""
    return HttpResponse("<h1>Welcome to Ayo Onipe!</h1>")
