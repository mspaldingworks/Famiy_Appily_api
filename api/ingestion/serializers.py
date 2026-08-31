from rest_framework import serializers

from .models import IngestedPosting


class IngestedPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngestedPosting
        fields = ["id", "source", "title", "company_name", "url", "raw_payload", "status", "created_at"]
        read_only_fields = ["status", "created_at"]
