import datetime

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Application, ApplicationEvent, Company, Contact
from .preparation import get_job, prepare_postings
from .serializers import ApplicationEventSerializer, ApplicationSerializer, CompanySerializer, ContactSerializer
from .sheets import SheetUnavailable, sync_sheet, sync_sheet_quietly


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = (
        Application.objects.select_related("company", "source_posting")
        .prefetch_related("events")
        .all()
    )
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    @action(detail=False, methods=["post"])
    def prepare(self, request):
        """
        Queue several postings for application in one go: generate materials,
        create the Application rows, and mark them ready to submit.

        Returns a job id immediately rather than blocking — generation is ~40s
        per posting and a batch would outlive any reasonable request timeout.
        """
        posting_ids = request.data.get("posting_ids") or []
        if not isinstance(posting_ids, list) or not posting_ids:
            return Response(
                {"detail": "Send posting_ids as a non-empty list."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(prepare_postings(posting_ids), status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=["get"], url_path=r"prepare/(?P<job_id>[0-9a-f]+)")
    def prepare_status(self, request, job_id=None):
        job = get_job(job_id)
        if job is None:
            return Response({"detail": "No such prepare job."}, status=status.HTTP_404_NOT_FOUND)
        return Response(job)

    @action(detail=True, methods=["post"], url_path="mark-applied")
    def mark_applied(self, request, pk=None):
        """Flip a queued application to applied and stamp the date."""
        application = self.get_object()
        application.status = Application.Status.APPLIED
        if not application.applied_date:
            application.applied_date = datetime.date.today()
        application.save(update_fields=["status", "applied_date"])
        sync_sheet_quietly()
        return Response(self.get_serializer(application).data)

    @action(detail=False, methods=["post"], url_path="sync-sheet")
    def sync_sheet_now(self, request):
        """Manual full rewrite of the Google Sheet, for the app's refresh button."""
        try:
            count = sync_sheet()
        except SheetUnavailable as error:
            return Response({"detail": str(error)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"synced": count})


class ApplicationEventViewSet(viewsets.ModelViewSet):
    queryset = ApplicationEvent.objects.all()
    serializer_class = ApplicationEventSerializer
