"""Artwork models."""

from django.db import models
from decimal import Decimal


class Artist(models.Model):
    """Representation of Artist."""

    name = models.CharField(max_length=255)
    bio = models.TextField(
        blank=True,
        help_text="Short biography of the artist.",
    )
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        """Represent Artist as string."""
        return f"Artist: {self.name}"


class Artwork(models.Model):
    """Representation of Artwork."""

    title = models.CharField(max_length=255)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="artworks",
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    creation_date = models.DateField(null=True, blank=True)
    discovered_date = models.DateField(null=True, blank=True)
    medium = models.CharField(
        max_length=255,
        help_text="E.g. Oil on Canvas, Sculpture, Digital Art",
    )
    image = models.ImageField(upload_to="artworks/", blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    is_for_sale = models.BooleanField(default=False)

    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Height in centimeters",
    )
    width = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Width in centimeters",
    )
    depth = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Depth in centimeters (for 3D art)",
    )

    def __str__(self):
        """Represent Artwork as string."""
        return f"Artwork: {self.title} by {self.artist.name}"

    def formatted_dimensions(self):
        """Format string of dimensions, omitting depth if irrelevant."""
        dims = f"{self.height} x {self.width} cm"
        if self.depth and self.depth > Decimal(0):
            dims += f" x {self.depth} cm (Depth)"
        return dims
