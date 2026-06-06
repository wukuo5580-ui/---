from django.contrib import admin
from .models import Category, Post, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "birth_date", "is_author")
    # search_fields = ("user__username", "bio") #查询


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}
    # search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "is_published",
        "created_at",
    )
    list_filter = ("category", "is_published")
    # search_fields = ("title", "content")
    filter_horizontal = ("likes",)