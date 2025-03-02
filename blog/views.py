"""Blog views."""

from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """Blog home view."""
    return HttpResponse("<h1>Blog Home.</h1>")
