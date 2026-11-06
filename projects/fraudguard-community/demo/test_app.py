import io
import unittest

from werkzeug.security import generate_password_hash

from fraudguard.app import create_app


CSV = b"transaction_id,customer_id,amount,timestamp,country,device_id,payment_method\nT-1,C-1,6000,2026-11-06T10:00:00,BO,D-1,card\n"


class AppTests(unittest.TestCase):
    def test_demo_and_export(self):
        app = create_app()
        app.config.update(TESTING=True, SECRET_KEY="fixture-secret")
        client = app.test_client()
        response = client.post("/demo", follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertIn(b"DEMO-100", response.data)
        exported = client.get("/export")
        self.assertIn(b"score,level,reasons", exported.data)

    def test_csv_upload(self):
        app = create_app()
        app.config.update(TESTING=True, SECRET_KEY="fixture-secret")
        response = app.test_client().post(
            "/upload",
            data={"file": (io.BytesIO(CSV), "operations.csv")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertIn(b"T-1", response.data)

    def test_lan_mode_requires_valid_key(self):
        app = create_app(lan_mode=True, access_key_hash=generate_password_hash("fixture-access-key"))
        app.config.update(TESTING=True, SECRET_KEY="fixture-secret")
        client = app.test_client()
        self.assertEqual(302, client.get("/").status_code)
        denied = client.post("/login", data={"access_key": "wrong"}, follow_redirects=True)
        self.assertIn(b"incorrecta", denied.data)
        accepted = client.post("/login", data={"access_key": "fixture-access-key"})
        self.assertEqual("/", accepted.headers["Location"])


if __name__ == "__main__":
    unittest.main()

