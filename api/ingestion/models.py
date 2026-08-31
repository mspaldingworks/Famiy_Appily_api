from django.db import models


class IngestedPosting(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        TRIAGED = "triaged", "Triaged"
        DISMISSED = "dismissed", "Dismissed"

    source = models.CharField(max_length=100, help_text="e.g. apify:indeed, rss:indeed, email")
    title = models.CharField(max_length=300)
    company_name = models.CharField(max_length=200, blank=True)
    # Job-board URLs routinely blow past URLField's 200-char default once
    # tracking/query params are attached, so this is widened deliberately.
    url = models.URLField(max_length=1000, blank=True)
    raw_payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # A recurring scrape re-sees the same jobs every run. Dedupe on
            # (source, url) regardless of status, so postings the user already
            # dismissed or promoted don't resurrect on the next run. Partial,
            # because blank URLs would otherwise all collide with each other.
            models.UniqueConstraint(
                fields=["source", "url"],
                condition=~models.Q(url=""),
                name="unique_posting_per_source_url",
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.source})"
