from django.db import models

# Create your models here.


class ContactSubmission(models.Model):
    """
    Model to store contact form submissions.

    Stores name, email, subject, message, submission timestamp, and status
    for managing contact requests.
    """

    STATUS_CHOICES = (
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.subject} - {self.email}"


class NewsletterSubscription(models.Model):
    """
    Model to store newsletter subscriptions.

    Tracks email, subscription date, and whether the subscription is active.
    """

    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-subscribed_at"]
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.email} - {status}"
