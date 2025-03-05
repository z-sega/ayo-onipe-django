"""Core Tags."""

from django import template

register = template.Library()


@register.simple_tag
def project_name():
    """Returns the name of the project."""
    return "My Django Project"


@register.filter
def uppercase(value):
    """Converts a string to uppercase."""
    return value.upper()
