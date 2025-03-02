"""Core views."""

from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """Core home view."""
    return render(request, "home.html")


def me(request):
    """Proprietor Info view."""
    return HttpResponse("<h1>Coming Soon: information about Ayo Onipe.</h1>")
