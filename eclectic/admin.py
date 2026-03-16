from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Publisher, Article, Newsletter

# 1. Custom User Admin to show the Role field
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Subscriptions', {'fields': ('role', 'subscribed_publishers', 'subscribed_journalists')}),
    )
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']

# 2. Article Admin with Approval Logic
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'is_approved', 'published_at']
    list_filter = ['is_approved', 'publisher', 'author']
    search_fields = ['title', 'content']
    # Requirement: Easy way for editors to approve articles
    actions = ['approve_articles']

    def approve_articles(self, request, queryset):
        queryset.update(is_approved=True)
    approve_articles.short_description = "Mark selected articles as Approved"

# 3. Standard Registration for other models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Publisher)
admin.site.register(Newsletter)