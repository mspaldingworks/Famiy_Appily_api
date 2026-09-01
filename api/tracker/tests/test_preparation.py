from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.authtoken.models import Token

from identity.models import ProfessionalProfile
from ingestion.models import IngestedPosting
from tracker.models import Application
from tracker.preparation import get_job, prepare_postings

MATERIALS = {
    "cover_letter": "Dear Hiring Team, ...",
    "resume_summary": "Development leader.",
    "resume_bullets": ["Grew Give for Good to $17,000"],
    "gaps": ["No PMP certification."],
    "unparsed": False,
}


def make_posting(url, title="Director of Development", score=90):
    return IngestedPosting.objects.create(
        source="apify:indeed",
        title=title,
        company_name="American Heart Association",
        url=url,
        apply_url=url + "/apply",
        score=score,
        raw_payload={"descriptionText": "x" * 500},
    )


@override_settings(ANTHROPIC_API_KEY="test-key", GOOGLE_SERVICE_ACCOUNT_FILE="", JOB_SHEET_ID="")
class PreparePostingsTests(TestCase):
    """prepare_postings runs its work on a thread; these call the body directly."""

    def setUp(self):
        ProfessionalProfile.objects.create(headline="Director", master_resume="Her background.")

    def run_prepare(self, posting_ids):
        # Run the thread body synchronously so assertions aren't racing it.
        with patch("tracker.preparation.threading.Thread") as thread:
            job = prepare_postings(posting_ids)
            target, args = thread.call_args.kwargs.get("target"), thread.call_args.kwargs.get("args")
            if target is None:
                target, args = thread.call_args[1]["target"], thread.call_args[1]["args"]
            target(*args)
        return get_job(job["id"])

    def test_creates_ready_applications_with_materials(self):
        posting = make_posting("https://example.test/job/1")
        with patch("ingestion.generation.generate_materials", return_value=MATERIALS) as gen:
            job = self.run_prepare([posting.pk])

        self.assertEqual(job["state"], "finished")
        self.assertEqual(job["done"], 1)
        self.assertTrue(job["results"][0]["ok"])
        gen.assert_called_once()

        application = Application.objects.get()
        self.assertEqual(application.status, Application.Status.READY)
        self.assertEqual(application.source_posting, posting)
        posting.refresh_from_db()
        self.assertEqual(posting.generated_materials["cover_letter"], MATERIALS["cover_letter"])

    def test_does_not_pay_to_regenerate_existing_materials(self):
        posting = make_posting("https://example.test/job/2")
        posting.generated_materials = MATERIALS
        posting.save(update_fields=["generated_materials"])

        with patch("ingestion.generation.generate_materials") as gen:
            self.run_prepare([posting.pk])

        gen.assert_not_called()

    def test_one_failure_does_not_lose_the_rest_of_the_batch(self):
        good = make_posting("https://example.test/job/3")
        missing_id = 999999
        with patch("ingestion.generation.generate_materials", return_value=MATERIALS):
            job = self.run_prepare([missing_id, good.pk])

        self.assertEqual(job["done"], 2)
        outcomes = {r["posting_id"]: r["ok"] for r in job["results"]}
        self.assertFalse(outcomes[missing_id])
        self.assertTrue(outcomes[good.pk])
        self.assertEqual(Application.objects.count(), 1)

    def test_queues_the_job_even_when_generation_is_unavailable(self):
        # A posting with no letter is still worth tracking; she can write one later.
        posting = make_posting("https://example.test/job/4")
        from ingestion.generation import GenerationUnavailable

        with patch("ingestion.generation.generate_materials", side_effect=GenerationUnavailable("no key")):
            job = self.run_prepare([posting.pk])

        self.assertTrue(job["results"][0]["ok"])
        self.assertIn("no key", job["results"][0]["detail"])
        self.assertEqual(Application.objects.get().status, Application.Status.READY)


@override_settings(ANTHROPIC_API_KEY="test-key", GOOGLE_SERVICE_ACCOUNT_FILE="", JOB_SHEET_ID="")
class ApplicationEndpointTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user("tester", password="x")
        self.auth = {"HTTP_AUTHORIZATION": f"Token {Token.objects.create(user=user).key}"}
        self.posting = make_posting("https://example.test/job/5")

    def test_prepare_returns_a_job_id_without_blocking(self):
        url = reverse("application-prepare")
        with patch("tracker.preparation.threading.Thread"):
            response = self.client.post(url, {"posting_ids": [self.posting.pk]},
                                        content_type="application/json", **self.auth)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json()["total"], 1)
        self.assertEqual(response.json()["state"], "running")

    def test_prepare_rejects_an_empty_list(self):
        url = reverse("application-prepare")
        response = self.client.post(url, {"posting_ids": []},
                                    content_type="application/json", **self.auth)
        self.assertEqual(response.status_code, 400)

    def test_mark_applied_sets_the_date(self):
        from ingestion.services import promote_posting_to_application

        application = promote_posting_to_application(self.posting)
        url = reverse("application-mark-applied", args=[application.pk])
        response = self.client.post(url, **self.auth)

        self.assertEqual(response.status_code, 200)
        application.refresh_from_db()
        self.assertEqual(application.status, Application.Status.APPLIED)
        self.assertIsNotNone(application.applied_date)

    def test_serializer_exposes_the_apply_url_and_materials(self):
        from ingestion.services import promote_posting_to_application

        self.posting.generated_materials = MATERIALS
        self.posting.save(update_fields=["generated_materials"])
        promote_posting_to_application(self.posting)

        response = self.client.get(reverse("application-list"), **self.auth)
        row = response.json()[0]
        self.assertEqual(row["apply_url"], self.posting.apply_url)
        self.assertEqual(row["generated_materials"]["cover_letter"], MATERIALS["cover_letter"])

    def test_requires_authentication(self):
        self.assertEqual(self.client.post(reverse("application-prepare")).status_code, 401)
