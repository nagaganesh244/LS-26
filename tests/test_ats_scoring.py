import unittest

from utils.keyword_matcher import match_keywords
from utils.score_calculator import calculate_ats_score


class AtsScoringTests(unittest.TestCase):
    def test_match_keywords_handles_common_variants(self):
        resume_text = "I built REST APIs and deployed cloud services for customers."
        matched, missing = match_keywords(resume_text, ["rest api", "cloud services", "docker"])

        self.assertIn("rest api", matched)
        self.assertIn("cloud services", matched)
        self.assertIn("docker", missing)

    def test_calculate_ats_score_is_not_too_punitive_for_average_matches(self):
        resume_text = "I developed reliable software using Python and SQL while improving delivery speed. " * 20
        result = calculate_ats_score(["python", "sql", "docker"], 10, resume_text)

        self.assertGreaterEqual(result["ats_score"], 45)
        self.assertGreaterEqual(result["keyword_score"], 30)


if __name__ == "__main__":
    unittest.main()
