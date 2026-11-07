import io
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from werkzeug.security import generate_password_hash

from fraudguard.app import create_app


CSV = b"transaction_id,merchant_id,expected_amount,charged_amount,currency,expected_status,actual_status,created_at,settled_at\nT-1,STORE-1,100,100,BOB,settled,declined,2026-11-06T10:00:00,\n"


class AppTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        factory = create_app
        isolated = patch(__name__ + '.create_app', side_effect=lambda **kwargs: factory(review_db=str(Path(temp.name) / 'tests.sqlite3'), **kwargs))
        isolated.start()
        self.addCleanup(isolated.stop)

    def test_demo_and_export(self):
        app = create_app()
        app.config.update(TESTING=True, CSRF_ENABLED=False, SECRET_KEY="fixture-secret")
        client = app.test_client()
        response = client.post("/demo", follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertIn(b"TX-1002", response.data)
        self.assertIn(b"rechazada o fall", response.data)
        exported = client.get("/export")
        self.assertIn(b"score,level,reasons", exported.data)

    def test_csv_upload(self):
        app = create_app()
        app.config.update(TESTING=True, CSRF_ENABLED=False, SECRET_KEY="fixture-secret")
        response = app.test_client().post(
            "/upload",
            data={"file": (io.BytesIO(CSV), "operations.csv")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertIn(b"T-1", response.data)

    def test_beginner_template_download(self):
        app = create_app()
        app.config.update(TESTING=True, CSRF_ENABLED=False, SECRET_KEY="fixture-secret")
        response = app.test_client().get("/plantilla")
        self.assertEqual(200, response.status_code)
        self.assertIn("plantilla_guardian.csv", response.headers["Content-Disposition"])
        self.assertIn(b"transaction_id,merchant_id,expected_amount", response.data)

    def test_rules_can_be_changed_without_code(self):
        app = create_app()
        app.config.update(TESTING=True, CSRF_ENABLED=False, SECRET_KEY="fixture-secret")
        client = app.test_client()
        response = client.post("/reglas", data={
            "high_amount": "1000",
            "velocity_count": "3",
            "velocity_minutes": "15",
            "country_window_minutes": "45",
            "shared_device_customers": "2",
        }, follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertIn(b"Reglas guardadas", response.data)
        client.post("/demo", follow_redirects=True)
        self.assertEqual("1000", str(app.config["ANALYSIS_SETTINGS"].high_amount))

    def test_profiles_have_downloadable_examples_and_audit_dashboard(self):
        app = create_app()
        app.config.update(TESTING=True, CSRF_ENABLED=False, SECRET_KEY="fixture-secret")
        client = app.test_client()
        self.assertIn(b"current_value,expected_value", client.get("/ejemplo/audit").data)
        response = client.post("/demo", data={"profile": "audit"}, follow_redirects=True)
        self.assertIn(b"Resumen de inconsistencias", response.data)
        self.assertIn(b"El valor actual no coincide con el esperado", response.data)

    def test_generic_example_profile_runs(self):
        app = create_app()
        app.config.update(TESTING=True, CSRF_ENABLED=False, SECRET_KEY="fixture-secret")
        client = app.test_client()
        response = client.post("/demo", data={"profile": "generic"}, follow_redirects=True)
        self.assertIn(b"Fila completamente duplicada", response.data)

    def test_two_source_reconciliation_and_review_inbox(self):
        app = create_app()
        app.config.update(TESTING=True, CSRF_ENABLED=False, SECRET_KEY="fixture-secret")
        client = app.test_client()
        sales = b"transaction_id,merchant_id,expected_amount,currency,expected_status\nTX-1,SHOP-1,120,BOB,settled\nTX-2,SHOP-2,50,BOB,settled\n"
        processor = b"transaction_id,charged_amount,currency,actual_status,settled_at\nTX-1,132,BOB,settled,2026-11-06T10:00:00\n"
        response = client.post("/conciliar", data={
            "sales_file": (io.BytesIO(sales), "ventas.csv"),
            "processor_file": (io.BytesIO(processor), "procesador.csv"),
        }, content_type="multipart/form-data", follow_redirects=True)
        self.assertIn(b"Importe distinto", response.data)
        self.assertIn(b"no aparece en el reporte del procesador", response.data)
        reviewed = client.post("/revisar/TX-1", data={"review_status": "Confirmada", "assigned_to": "Ana", "note": "Validado con reporte"}, follow_redirects=True)
        self.assertIn(b"Confirmada", reviewed.data)
        app.config["RESULTS"][0]["record_id"] = "TX-1"
        view = client.get("/")
        self.assertIn(b"cambios", view.data)

    def test_reconciliation_recognizes_spanish_provider_headers_and_duplicates(self):
        app = create_app()
        app.config.update(TESTING=True, CSRF_ENABLED=False, SECRET_KEY="fixture-secret")
        client = app.test_client()
        sales = b"Referencia,Comercio,Importe esperado,Divisa,Estado esperado\nR-1,Tienda,50,BOB,Pagado\nR-1,Tienda,50,BOB,Pagado\n"
        processor = b"ID de pago,Monto cobrado,Moneda,Estado del pago,Fecha de liquidacion\nR-1,50,BOB,Acreditado,2026-11-06T10:00:00\n"
        response = client.post("/conciliar", data={
            "sales_file": (io.BytesIO(sales), "ventas.csv"),
            "processor_file": (io.BytesIO(processor), "procesador.csv"),
        }, content_type="multipart/form-data", follow_redirects=True)
        self.assertIn("venta repite esta referencia".encode(), response.data.lower())

    def test_lan_mode_requires_valid_key(self):
        app = create_app(lan_mode=True, access_key_hash=generate_password_hash("fixture-access-key"))
        app.config.update(TESTING=True, CSRF_ENABLED=False, SECRET_KEY="fixture-secret")
        client = app.test_client()
        self.assertEqual(302, client.get("/").status_code)
        denied = client.post("/login", data={"access_key": "wrong"}, follow_redirects=True)
        self.assertIn(b"incorrecta", denied.data)
        accepted = client.post("/login", data={"access_key": "fixture-access-key"})
        self.assertEqual("/", accepted.headers["Location"])


if __name__ == "__main__":
    unittest.main()

