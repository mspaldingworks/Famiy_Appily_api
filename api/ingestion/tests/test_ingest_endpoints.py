from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.authtoken.models import Token

from ingestion.models import IngestedPosting

TEST_KEY = "test-ingestion-key"


@override_settings(INGESTION_API_KEY=TEST_KEY)
class IngestViewTests(TestCase):
    def setUp(self):
        self.url = reverse("ingest")

    def test_accepts_a_single_posting(self):
        response = self.client.post(
            self.url,
            data={"source": "email", "title": "Analyst", "company_name": "Acme"},
            content_type="application/json",
            HTTP_X_INGESTION_KEY=TEST_KEY,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(IngestedPosting.objects.count(), 1)

    def test_accepts_a_batch(self):
        response = self.client.post(
            self.url,
            data=[
                {"source": "email", "title": "Analyst"},
                {"source": "email", "title": "Coordinator"},
            ],
            content_type="application/json",
            HTTP_X_INGESTION_KEY=TEST_KEY,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(IngestedPosting.objects.count(), 2)

    def test_url_stays_optional(self):
        # Email-sourced postings have no URL. The (source, url) unique constraint
        # must not make DRF demand one.
        response = self.client.post(
            self.url,
            data={"source": "email", "title": "Analyst"},
            content_type="application/json",
            HTTP_X_INGESTION_KEY=TEST_KEY,
        )
        self.assertEqual(response.status_code, 201)

    def test_resending_the_same_posting_returns_409_not_500(self):
        payload = {"source": "apify:indeed", "title": "Analyst", "url": "https://x.test/1"}
        first = self.client.post(
            self.url, data=payload, content_type="application/json", HTTP_X_INGESTION_KEY=TEST_KEY
        )
        second = self.client.post(
            self.url, data=payload, content_type="application/json", HTTP_X_INGESTION_KEY=TEST_KEY
        )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 409)
        self.assertEqual(IngestedPosting.objects.count(), 1)

    def test_rejects_a_bad_key(self):
        response = self.client.post(
            self.url,
            data={"source": "email", "title": "Analyst"},
            content_type="application/json",
            HTTP_X_INGESTION_KEY="wrong",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(IngestedPosting.objects.count(), 0)


class PostingStatusFilterTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user("tester", password="x")
        self.token = Token.objects.create(user=user)
        IngestedPosting.objects.create(source="apify:indeed", title="New one", url="https://x.test/1")
        IngestedPosting.objects.create(
            source="apify:indeed",
            title="Old one",
            url="https://x.test/2",
            status=IngestedPosting.Status.DISMISSED,
        )

    def test_filters_by_status(self):
        # The Job Feed asks for new postings only, so it doesn't have to pull
        # every posting ever scraped once daily runs pile up.
        response = self.client.get(
            reverse("ingestedposting-list") + "?status=new",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)
        titles = [row["title"] for row in response.json()]
        self.assertEqual(titles, ["New one"])

    def test_returns_everything_without_the_filter(self):
        response = self.client.get(
            reverse("ingestedposting-list"),
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(len(response.json()), 2)
