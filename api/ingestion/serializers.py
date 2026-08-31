from rest_framework import serializers

from .models import IngestedPosting


class IngestedPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngestedPosting
        fields = ["id", "source", "title", "company_name", "url", "raw_payload", "status", "created_at"]
        read_only_fields = ["status", "created_at"]
        # The model's partial UniqueConstraint(source, url) makes DRF generate a
        # UniqueTogetherValidator, which would force every caller to send a url —
        # but email-sourced postings legitimately have none. Deduping is the DB
        # constraint's job (and ingest_items' for scraped batches); the view
        # turns the resulting IntegrityError into a 409.
        validators = []
