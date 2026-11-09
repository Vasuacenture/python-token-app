import unittest

from app import app


class TokenAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_homepage_renders_form(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create a new token", response.data)

    def test_creates_token_for_valid_label(self):
        response = self.client.post(
            "/api/token",
            json={"label": "staging environment"},
        )
        body = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(body["success"])
        self.assertEqual(body["label"], "staging environment")
        self.assertIsInstance(body["token"], str)
        self.assertGreaterEqual(len(body["token"]), 40)

    def test_trims_label(self):
        response = self.client.post("/api/token", json={"label": "  demo  "})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["label"], "demo")

    def test_rejects_missing_or_blank_label(self):
        for payload in ({}, {"label": "   "}):
            with self.subTest(payload=payload):
                response = self.client.post("/api/token", json=payload)

                self.assertEqual(response.status_code, 400)
                self.assertFalse(response.get_json()["success"])

    def test_rejects_non_string_label(self):
        response = self.client.post("/api/token", json={"label": 123})

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_rejects_label_over_100_characters(self):
        response = self.client.post("/api/token", json={"label": "x" * 101})

        self.assertEqual(response.status_code, 400)
        self.assertIn("100 characters", response.get_json()["error"])

    def test_rejects_non_json_request_with_json_error(self):
        response = self.client.post("/api/token", data="label=demo")

        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get_json()["success"], False)

    def test_rejects_json_array(self):
        response = self.client.post("/api/token", json=["demo"])

        self.assertEqual(response.status_code, 400)
        self.assertIn("object", response.get_json()["error"])

    def test_returns_json_for_malformed_json(self):
        response = self.client.post(
            "/api/token",
            data="{",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.get_json()["success"])


if __name__ == "__main__":
    unittest.main()
