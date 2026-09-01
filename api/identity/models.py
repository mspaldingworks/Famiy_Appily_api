from django.db import models


class ProfessionalProfile(models.Model):
    """Single-row bio/summary. Intended usage: exactly one instance via the admin."""

    headline = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    # Canonical career history in plain text — the source material the
    # application-materials generator tailors from. Kept as one field rather
    # than a normalized schema because it's fed to a model as prose, and
    # over-structuring it would lose the phrasing she actually uses.
    master_resume = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "professional profile"

    def __str__(self):
        return self.headline or "Professional profile"


class Skill(models.Model):
    class Proficiency(models.TextChoices):
        LEARNING = "learning", "Learning"
        COMPETENT = "competent", "Competent"
        STRONG = "strong", "Strong"
        EXPERT = "expert", "Expert"

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)
    proficiency = models.CharField(max_length=20, choices=Proficiency.choices, default=Proficiency.COMPETENT)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class ProfileLink(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        NEEDS_UPDATE = "needs_update", "Needs update"
        STALE = "stale", "Stale"

    platform = models.CharField(max_length=100)
    url = models.URLField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    notes = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["platform"]

    def __str__(self):
        return f"{self.platform} ({self.get_status_display()})"


class ResumeVersion(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="identity/resumes/")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
