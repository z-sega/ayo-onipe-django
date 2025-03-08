from django.contrib import admin
from django import forms
from .models import Post


class PostAdminForm(forms.ModelForm):
    """Admin form for Post that updates the title and slug dynamically."""

    class Meta:
        model = Post
        fields = "__all__"


class PostAdmin(admin.ModelAdmin):
    """Custom Django Admin for Post."""

    form = PostAdminForm
    list_display = ("title", "slug", "created")  # Customize display
    readonly_fields = ("html_content",)  # HTML content is auto-generated

    fieldsets = (
        (None, {"fields": ("org_content", "html_content")}),
        ("Metadata", {"fields": ("title", "slug")}),
    )


admin.site.register(Post, PostAdmin)
