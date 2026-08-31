from rest_framework import serializers

from .models import Application, ApplicationEvent, Company, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "company", "name", "role", "email", "phone", "notes"]


class CompanySerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ["id", "name", "website", "notes", "created_at", "contacts"]


class ApplicationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationEvent
        fields = ["id", "application", "note", "occurred_at"]
        read_only_fields = ["occurred_at"]


class ApplicationSerializer(serializers.ModelSerializer):
    events = ApplicationEventSerializer(many=True, read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id", "company", "company_name", "role_title", "job_url", "status", "source",
            "applied_date", "salary_notes", "resume", "cover_letter", "notes",
            "created_at", "updated_at", "events",
        ]
