"""Core views."""

from django.urls import get_resolver, URLPattern, URLResolver
from django.urls import reverse
from django.views.generic import View
from django.views.generic.base import TemplateView

from django.utils.functional import cached_property
from typing import List, Union, Dict

from view_breadcrumbs import BaseBreadcrumbMixin


class IndexView(BaseBreadcrumbMixin, TemplateView):
    template_name = "index.html"

    @cached_property
    def crumbs(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MeView(BaseBreadcrumbMixin, TemplateView):
    template_name = "me.html"

    @cached_property
    def crumbs(self):
        return [("Me", reverse("me"))]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["personal_info"] = {
            "name": "Ayo Onipe",
            "occupation": "Software Developer",
            "education": {
                "repr": "BT, Automation Systems Engineering. McMaster University",
                "link": "https://www.eng.mcmaster.ca/sept/degree-options/automation-systems-engineering-technology/",
            },
        }
        context["contact_info"] = {
            "email": {"repr": "mail@ayoonipe.com", "link": "mailto: mail@ayoonipe.com"},
            "phone": "+1 905 962 9762",
            "github": {"repr": "z-sega", "link": "https://github.com/z-sega"},
            "linkedin": {
                "repr": "Ayo Onipe",
                "link": "https://www.linkedin.com/in/ayo-onipe-5b5b3b152/",
            },
        }
        return context


class SiteMapView(BaseBreadcrumbMixin, TemplateView):
    """Site Map View."""

    template_name = "site_map.html"

    def extract_url_tree(
        self, urlpatterns: List[Union[URLPattern, URLResolver]], base_path: str = ""
    ) -> List[Dict[str, Union[str, List]]]:
        """Recursively extracts URL patterns into a structured tree."""
        tree = []

        for pattern in urlpatterns:
            if isinstance(pattern, URLPattern):  # Regular URL
                full_path = f"{base_path}{pattern.pattern}".replace("^", "").replace(
                    "$", ""
                )
                absolute_path = f"/{full_path}".replace("//", "/")  # Ensure leading `/`
                tree.append({"name": pattern.name or full_path, "path": absolute_path})
            elif isinstance(pattern, URLResolver):  # Nested URLs
                sub_tree = self.extract_url_tree(
                    pattern.url_patterns, f"{base_path}{pattern.pattern}"
                )
                tree.append({"name": pattern.pattern, "sub_paths": sub_tree})
        return tree

    @cached_property
    def crumbs(self):
        return [("Site Map", reverse("site_map"))]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url_tree"] = self.extract_url_tree(get_resolver().url_patterns)[
            1:
        ]  # skip admin
        return context
