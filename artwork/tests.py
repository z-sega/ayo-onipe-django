"""Artwork tests."""

from decimal import Decimal
from datetime import date
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Artist, Artwork
from .services import (
    validate_discovered_date,
    validate_dimensions,
    create_artist,
    create_artwork,
)


class ArtworkServicesTestCase(TestCase):
    """Test suite for Artwork services."""

    def test_validate_discovered_date_valid(self):
        """Test that a discovered date later than or equal to creation date is valid."""
        try:
            validate_discovered_date(
                creation_date=date(2020, 1, 1),
                discovered_date=date(2021, 1, 1),
            )
        except ValidationError:
            self.fail("Validation unexpectedly failed for a valid date.")

    def test_validate_discovered_date_invalid(self):
        """Test that a discovered date earlier than creation date raises an error."""
        with self.assertRaises(ValidationError) as context:
            validate_discovered_date(
                creation_date=date(2021, 1, 1),
                discovered_date=date(2020, 1, 1),
            )
        self.assertEqual(
            str(context.exception),
            "['Discovered date cannot be earlier than creation date.']",
        )

    def test_validate_dimensions_valid(self):
        """Test that positive dimensions pass validation."""
        try:
            validate_dimensions(
                height=Decimal("10.5"),
                width=Decimal("20.0"),
                depth=Decimal("5.0"),
            )
        except ValidationError:
            self.fail("Validation unexpectedly failed for valid dimensions.")

    def test_validate_dimensions_invalid(self):
        """Test that zero or negative dimensions raise a validation error."""
        invalid_cases = [
            {
                "height": Decimal("-1.0"),
                "width": Decimal("20.0"),
                "depth": Decimal("5.0"),
            },
            {
                "height": Decimal("10.0"),
                "width": Decimal("-2.0"),
                "depth": Decimal("5.0"),
            },
            {
                "height": Decimal("10.0"),
                "width": Decimal("20.0"),
                "depth": Decimal("-5.0"),
            },
            {"height": Decimal("0"), "width": Decimal("20.0"), "depth": Decimal("5.0")},
        ]

        for case in invalid_cases:
            with self.assertRaises(ValidationError) as context:
                validate_dimensions(**case)
            self.assertIn(
                "must be a positive number",
                str(context.exception),
            )

    def test_create_artist_success(self):
        """Test successful artist creation."""
        artist = create_artist(
            name="Vincent van Gogh",
            bio="A Dutch post-impressionist painter.",
            birth_date=date(1853, 3, 30),
            website="https://vangogh.com",
            country="Netherlands",
        )

        self.assertEqual(artist.name, "Vincent van Gogh")
        self.assertEqual(artist.country, "Netherlands")

    def test_create_artist_missing_name(self):
        """Test that missing artist name raises an error."""
        with self.assertRaises(ValidationError):
            create_artist(
                name="",
                bio="Unknown artist.",
                birth_date=date(1900, 1, 1),
                website=None,
                country="Unknown",
            )

    def test_create_artwork_success(self):
        """Test successful artwork creation."""
        artist = create_artist(
            name="Claude Monet",
            bio="A founder of French Impressionist painting.",
            birth_date=date(1840, 11, 14),
            website="https://monet.com",
            country="France",
        )

        artwork = create_artwork(
            title="Water Lilies",
            artist=artist,
            description="A series of paintings by Monet.",
            creation_date=date(1900, 6, 1),
            discovered_date=date(1901, 1, 1),
            medium="Oil on canvas",
            price=Decimal("1500000.00"),
            is_for_sale=True,
            height=Decimal("150"),
            width=Decimal("200"),
            depth=None,
        )

        self.assertEqual(artwork.title, "Water Lilies")
        self.assertEqual(artwork.artist, artist)
        self.assertTrue(artwork.is_for_sale)
        self.assertEqual(artwork.medium, "Oil on canvas")

    def test_create_artwork_invalid_discovered_date(self):
        """Test that an artwork with a discovered date before creation date raises an error."""
        artist = create_artist(
            name="Pablo Picasso", bio="Spanish painter", country="Spain"
        )

        with self.assertRaises(ValidationError) as context:
            create_artwork(
                title="Guernica",
                artist=artist,
                creation_date=date(1937, 4, 1),
                discovered_date=date(1936, 12, 1),  # Invalid
                medium="Oil on canvas",
            )
        self.assertIn(
            "Discovered date cannot be earlier than creation date",
            str(context.exception),
        )

    def test_create_artwork_invalid_dimensions(self):
        """Test that artworks with zero or negative dimensions raise an error."""
        artist = create_artist(
            name="Georgia O'Keeffe", bio="American artist", country="USA"
        )

        with self.assertRaises(ValidationError) as context:
            create_artwork(
                title="Red Canna",
                artist=artist,
                creation_date=date(1924, 1, 1),
                discovered_date=date(1925, 1, 1),
                medium="Oil on canvas",
                height=Decimal("-5"),  # Invalid
                width=Decimal("100"),
                depth=Decimal("10"),
            )
        self.assertIn("Height must be a positive number", str(context.exception))

    def test_create_artwork_without_artist(self):
        """Test creating an artwork without an associated artist."""
        artwork = create_artwork(
            title="Mysterious Painting",
            description="An anonymous masterpiece.",
            creation_date=date(1800, 1, 1),
            discovered_date=date(1810, 1, 1),
            medium="Oil on wood",
        )

        self.assertIsNone(artwork.artist)
        self.assertEqual(artwork.title, "Mysterious Painting")
