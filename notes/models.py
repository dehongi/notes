from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-updated_at"]


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.user.get_full_name()} on {self.note.title}"

    class Meta:
        ordering = ["-created_at"]

    def get_creation_time(self):
        """Return a human-friendly creation time."""
        now = timezone.now()
        diff = now - self.created_at

        if diff.days == 0:
            if diff.seconds < 60:
                return "just now"
            if diff.seconds < 3600:
                return f"{diff.seconds // 60} minutes ago"
            return f"{diff.seconds // 3600} hours ago"
        if diff.days == 1:
            return "yesterday"
        if diff.days < 7:
            return f"{diff.days} days ago"
        return self.created_at.strftime("%b %d, %Y")
