"""Artwork services."""

from typing import Optional
from decimal import Decimal

from datetime import date
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Artist, Artwork


def validate_discovered_date(
    creation_date: date,
    discovered_date: date,
) -> None:
    """
    Validate that `discovered_date` is not earlier than `creation_date`.

    Args:
        creation_date (date): The date when the artwork was created.
        discovered_date (date): The date when the artwork was discovered.

    Raises:
        ValidationError: If discovered_date is earlier than creation_date.
    """
    if discovered_date and creation_date and discovered_date < creation_date:
        raise ValidationError("Discovered date cannot be earlier than creation date.")


def validate_dimensions(
    height: Decimal,
    width: Decimal,
    depth: Decimal,
) -> None:
    """
    Validate that height, width, and depth (if provided) are positive numbers.

    Args:
        height (Decimal): Height of the artwork in cm.
        width (Decimal): Width of the artwork in cm.
        depth (Decimal): Depth of the artwork in cm.

    Raises:
        ValidationError: If any dimension is negative or zero.
    """
    dims = {"height": height, "width": width, "depth": depth}

    for field_name, value in dims.items():
        if value is not None and value <= Decimal(0):
            raise ValidationError(
                f"{field_name.capitalize()} must be a positive number."
            )


@transaction.atomic
def create_artist(
    *,
    name: str,
    bio: Optional[str] = "",
    birth_date: Optional[date] = None,
    website: Optional[str] = None,
    country: Optional[str] = None,
) -> Artist:
    """
    Create or retrieve an artist.

    Args:
        name (str): Artist's name.
        bio (Optional[str]): Biography.
        birth_date (Optional[date]): Date of birth.
        website (Optional[str]): Website URL.
        country (Optional[str]): Country of origin.

    Returns:
        Artist: The created or retrieved artist instance.
    """
    artist = Artist(
        name=name,
        bio=bio,
        birth_date=birth_date,
        website=website,
        country=country,
    )
    artist.full_clean()
    artist.save()

    return artist


@transaction.atomic
def create_artwork(
    *,
    title: str,
    artist: Optional[Artist] = None,
    description: Optional[str] = "",
    creation_date: Optional[date] = None,
    discovered_date: Optional[date] = None,
    medium: str,
    image: Optional[str] = None,
    price: Optional[Decimal] = None,
    is_for_sale: bool = False,
    height: Optional[Decimal] = None,
    width: Optional[Decimal] = None,
    depth: Optional[Decimal] = None,
) -> Artwork:
    """
    Create an artwork entry.

    Args:
        title (str): Title of the artwork.
        artist (Optional[Artist]): Associated artist (nullable).
        description (Optional[str]): Artwork description.
        creation_date (Optional[date]): Date of creation.
        discovered_date (Optional[date]): Date it was discovered.

    Returns:
        Artwork: The created artwork instance.
    """
    validate_discovered_date(creation_date, discovered_date)
    validate_dimensions(height, width, depth)

    artwork = Artwork(
        title=title,
        artist=artist,
        description=description,
        creation_date=creation_date,
        discovered_date=discovered_date,
        medium=medium,
        image=image,
        price=price,
        is_for_sale=is_for_sale,
        height=height,
        width=width,
        depth=depth,
    )
    artwork.full_clean()
    artwork.save()

    return artwork
