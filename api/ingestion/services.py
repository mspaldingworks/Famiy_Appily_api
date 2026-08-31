from tracker.models import Application, Company

from .models import IngestedPosting


def promote_posting_to_application(posting: IngestedPosting) -> Application:
    """Create a tracker Application from an ingested posting and mark it triaged."""
    company_name = posting.company_name or "Unknown"
    company, _ = Company.objects.get_or_create(name=company_name)
    application = Application.objects.create(
        company=company,
        role_title=posting.title,
        job_url=posting.url,
        source=Application.Source.INGESTED,
        notes=f"Promoted from ingested posting (source: {posting.source}).",
    )
    posting.status = IngestedPosting.Status.TRIAGED
    posting.save(update_fields=["status"])
    return application
