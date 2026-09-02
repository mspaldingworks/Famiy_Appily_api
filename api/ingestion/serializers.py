from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import IngestedPosting


class IngestedPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngestedPosting
        fields = ["id", "source", "title", "company_name", "url", "apply_url", "raw_payload",
                  "status", "score", "score_reasons", "created_at"]
        read_only_fields = ["status", "created_at", "score", "score_reasons"]
        # Meta-level validators only; the url field also gets its own
        # UniqueValidator from the model constraint — cleared in __init__ below.
        validators = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The model's partial UniqueConstraint on url makes DRF attach a
        # UniqueValidator to the field, which does a lookup and rejects a repeat
        # with 400 before it ever reaches the database. That breaks two things:
        # email-sourced postings legitimately have no url and would all collide,
        # and callers expect a 409 for "already have this one", which the view
        # produces from the IntegrityError. Deduping stays the DB's job.
        self.fields["url"].validators = [
            v for v in self.fields["url"].validators
            if not isinstance(v, UniqueValidator)
        ]
