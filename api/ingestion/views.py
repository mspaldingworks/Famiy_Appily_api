from django.conf import settings
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker.serializers import ApplicationSerializer

from .models import IngestedPosting
from .serializers import IngestedPostingSerializer
from .services import promote_posting_to_application


class IngestedPostingViewSet(viewsets.ModelViewSet):
    """Browsing/triage of ingested postings from the native app."""

    queryset = IngestedPosting.objects.all()
    serializer_class = IngestedPostingSerializer

    @action(detail=True, methods=["post"])
    def promote(self, request, pk=None):
        posting = self.get_object()
        if posting.status == IngestedPosting.Status.TRIAGED:
            return Response(
                {"detail": "This posting was already promoted to an application."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        application = promote_posting_to_application(posting)
        return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)


class IngestView(APIView):
    """
    Webhook target for external automation (e.g. a Hostinger-hosted n8n workflow)
    to push in scraped/RSS/email-sourced job postings. Authenticated via a shared
    secret in the X-Ingestion-Key header rather than a user session, since the
    caller is a single trusted external workflow, not an end user.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        provided_key = request.headers.get("X-Ingestion-Key", "")
        if not settings.INGESTION_API_KEY or provided_key != settings.INGESTION_API_KEY:
            return Response({"detail": "Invalid or missing ingestion key."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = IngestedPostingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
