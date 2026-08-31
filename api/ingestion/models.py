from django.db import models


class IngestedPosting(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        TRIAGED = "triaged", "Triaged"
        DISMISSED = "dismissed", "Dismissed"

    source = models.CharField(max_length=100, help_text="e.g. rss:indeed, email, n8n-scraper-x")
    title = models.CharField(max_length=300)
    company_name = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    raw_payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.source})"
