from django.test import SimpleTestCase

from ingestion.scoring import score_posting


def posting(**overrides):
    base = {
        "title": "Coordinator",
        "companyName": "Some Company",
        "descriptionText": "",
        "location": {"city": "Louisville", "formattedAddressShort": "Louisville, KY"},
        "isRemote": False,
        "age": "10 days ago",
    }
    base.update(overrides)
    return base


class ScoringTests(SimpleTestCase):
    def test_a_real_match_outranks_the_noise_indeed_returns(self):
        # The actual failure mode: a "director of development" search returning
        # nursing roles. The real one has to win by a wide margin.
        good, _ = score_posting(posting(
            title="Director of Development",
            companyName="Louisville Urban League",
            descriptionText="Lead fundraising, grant writing, and donor stewardship for our nonprofit.",
        ))
        noise, _ = score_posting(posting(title="RN/LPN", companyName="Sansbury Care Center"))
        self.assertGreater(good, noise + 40)

    def test_each_lane_is_recognized(self):
        for title in ["Director of Development", "Grant Writer", "Communications Manager",
                      "Digital Content Specialist", "Program Director"]:
            score, reasons = score_posting(posting(title=title))
            self.assertTrue(
                any("lane" in reason for reason in reasons),
                f"{title!r} should match a lane, got {reasons}",
            )

    def test_clinical_and_trades_roles_are_pushed_down(self):
        for title in ["Registered Nurse", "CDL Truck Driver", "Construction Supervisor",
                      "Pharmacy Technician", "Line Cook"]:
            score, reasons = score_posting(posting(title=title))
            self.assertLess(score, 35, f"{title!r} scored {score}")
            self.assertTrue(any("noise" in reason for reason in reasons))

    def test_remote_and_local_both_score_well_but_distant_onsite_does_not(self):
        remote, _ = score_posting(posting(title="Grant Writer", isRemote=True, location={"city": ""}))
        local, _ = score_posting(posting(title="Grant Writer"))
        distant, _ = score_posting(posting(
            title="Grant Writer",
            location={"city": "Phoenix", "formattedAddressShort": "Phoenix, AZ"},
        ))
        self.assertGreater(remote, distant)
        self.assertGreater(local, distant)

    def test_hourly_roles_are_penalized_without_inventing_a_target_salary(self):
        hourly, reasons = score_posting(posting(
            title="Program Coordinator",
            salary={"salaryType": "hourly", "salaryText": "From $20 an hour"},
        ))
        salaried, _ = score_posting(posting(
            title="Program Coordinator",
            salary={"salaryType": "yearly", "salaryMax": 75000},
        ))
        self.assertGreater(salaried, hourly)
        self.assertIn("Hourly wage role", reasons)

    def test_junior_titles_rank_below_the_same_role_at_her_level(self):
        senior, _ = score_posting(posting(title="Development Director"))
        junior, _ = score_posting(posting(title="Development Assistant"))
        self.assertGreater(senior, junior)

    def test_nonprofit_employers_get_credit(self):
        with_signal, reasons = score_posting(posting(
            title="Communications Manager",
            descriptionText="Our nonprofit foundation serves youth across the community.",
        ))
        without, _ = score_posting(posting(title="Communications Manager"))
        self.assertGreater(with_signal, without)
        self.assertTrue(any("Nonprofit" in reason for reason in reasons))

    def test_fresh_postings_edge_out_stale_ones(self):
        fresh, _ = score_posting(posting(title="Grant Writer", age="1 day ago"))
        stale, _ = score_posting(posting(title="Grant Writer", age="21 days ago"))
        self.assertGreater(fresh, stale)

    def test_score_always_lands_in_range_and_reasons_are_readable(self):
        for item in [posting(), posting(title="RN"), posting(title="Director of Development"), {}]:
            score, reasons = score_posting(item)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)
            self.assertIsInstance(reasons, list)
