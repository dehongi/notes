from django.contrib import admin
from .models import ContactSubmission, NewsletterSubscription


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for ContactSubmission model."""

    list_display = ("subject", "name", "email", "created_at", "status")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "subject", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    fieldsets = (
        (None, {"fields": ("status",)}),
        ("Contact Information", {"fields": ("name", "email")}),
        ("Message Details", {"fields": ("subject", "message", "created_at")}),
    )


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    """Admin configuration for NewsletterSubscription model."""

    list_display = ("email", "subscribed_at", "is_active")
    list_filter = ("is_active", "subscribed_at")
    search_fields = ("email",)
    readonly_fields = ("subscribed_at",)
    actions = ["activate_subscriptions", "deactivate_subscriptions"]

    def activate_subscriptions(self, request, queryset):
        """Activate selected subscriptions."""
        queryset.update(is_active=True)
        self.message_user(
            request, f"{queryset.count()} subscriptions have been activated."
        )

    activate_subscriptions.short_description = "Activate selected subscriptions"

    def deactivate_subscriptions(self, request, queryset):
        """Deactivate selected subscriptions."""
        queryset.update(is_active=False)
        self.message_user(
            request, f"{queryset.count()} subscriptions have been deactivated."
        )

    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"
