from rest_framework import viewsets

from .models import Application, ApplicationEvent, Company, Contact
from .serializers import ApplicationEventSerializer, ApplicationSerializer, CompanySerializer, ContactSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related("company").prefetch_related("events").all()
    serializer_class = ApplicationSerializer


class ApplicationEventViewSet(viewsets.ModelViewSet):
    queryset = ApplicationEvent.objects.all()
    serializer_class = ApplicationEventSerializer
