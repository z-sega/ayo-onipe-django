"""User views."""

from django.http import HttpResponse


def me(request):
    """Proprietor Info view."""
    return HttpResponse("<h1>Coming Soon: information about Ayo Onipe.</h1>")
