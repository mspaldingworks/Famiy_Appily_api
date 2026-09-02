from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .ats import describe
from .models import IngestedPosting


class IngestedPostingSerializer(serializers.ModelSerializer):
    # Which ATS this applies through, and whether it will demand an account
    # before showing the form — the feed flags those so she isn't sent to a
    # wall from her phone.
    platform = serializers.SerializerMethodField()
    requires_account = serializers.SerializerMethodField()
    sign_in_url = serializers.SerializerMethodField()

    def _ats(self, posting):
        return describe(posting.apply_url or posting.url)

    def get_platform(self, posting):
        return self._ats(posting)["platform"]

    def get_requires_account(self, posting):
        return self._ats(posting)["requires_account"]

    def get_sign_in_url(self, posting):
        return self._ats(posting)["sign_in_url"]

    class Meta:
        model = IngestedPosting
        fields = ["id", "source", "title", "company_name", "url", "apply_url", "raw_payload",
                  "status", "score", "score_reasons", "created_at",
                  "platform", "requires_account", "sign_in_url"]
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
