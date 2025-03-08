"""Blog models."""

from django.db import models
from django.urls import reverse

from model_utils.models import TimeStampedModel

import re
import subprocess


class Post(TimeStampedModel):
    """Represent Blog Post."""

    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    org_content = models.TextField(help_text="Raw Org-mode content")
    html_content = models.TextField(
        editable=False, help_text="Generated HTML content from Org-mode"
    )

    def get_absolute_url(self):
        """Returns the absolute URL for this blog post."""
        return reverse("post_detail", kwargs={"slug": self.slug})

    def extract_org_metadata(self):
        """Extract metadata (title, author, etc.) from Org-mode content."""
        metadata = {}
        for line in self.org_content.splitlines():
            match = re.match(
                r"^\#\+(\w+):\s*(.+)$", line
            )  # Matches lines like #+TITLE: My Blog
            if match:
                key, value = match.groups()
                metadata[key.lower()] = value  # Store as lowercase keys
        return metadata

    def convert_org_to_html(self):
        """Convert Org-mode content to HTML using Pandoc."""
        try:
            result = subprocess.run(
                ["pandoc", "-f", "org", "-t", "html"],
                input=self.org_content,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"<p>Error converting Org file: {e}</p>"

    def save(self, *args, **kwargs):
        """
        Save blog.

        Extract metadata, update title/slug,
        and convert Org to HTML before saving.
        """
        metadata = self.extract_org_metadata()

        # Auto-set title if found in Org metadata
        if "title" in metadata and not self.title:
            self.title = metadata["title"]

        # Auto-generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.title)

        # Convert Org to HTML
        self.html_content = self.convert_org_to_html()
        super().save(*args, **kwargs)

    def __str__(self):
        """Represent blog as string."""
        return self.title or "Untitled Blog Post"

    class Meta:
        verbose_name = "Post"
