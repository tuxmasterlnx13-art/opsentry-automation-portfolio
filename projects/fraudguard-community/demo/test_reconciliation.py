import io
from pathlib import Path
import tempfile
import unittest

from fraudguard.app import create_app
from fraudguard.reconciliation import money, read_report, reconcile


SALES = b'reference,merchant,amount,currency,status\nA-1,SHOP,120.00,BOB,settled\n'
PROCESSOR = b'payment_id,amount,currency,status,paid_at\nA-1,120.00,BOB,settled,2026-11-06T10:00:00\n'


class ReconciliationTests(unittest.TestCase):
    def test_approved_is_not_settled(self):
        sales = read_report(SALES)
        processor = read_report(PROCESSOR.replace(b'settled,2026', b'approved,2026'))
        result = reconcile(sales, processor)[0]
        self.assertIn('not_settled', result['codes'])

    def test_unknown_status_and_currency_are_not_silently_accepted(self):
        result = reconcile(read_report(SALES), read_report(PROCESSOR.replace(b'BOB,settled', b',mystery')))[0]
        self.assertIn('unknown_status', result['codes'])
        self.assertIn('invalid_currency', result['codes'])

    def test_empty_reference_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'referencia vacía'):
            reconcile(read_report(SALES.replace(b'A-1', b'')), read_report(PROCESSOR))

    def test_duplicate_sales_are_ambiguous_not_overwritten(self):
        rows = read_report(SALES)
        result = reconcile(rows + rows, read_report(PROCESSOR))[0]
        self.assertEqual(2, result['sales_rows'])
        self.assertIn('duplicate_sale', result['codes'])

    def test_money_supports_both_decimal_conventions_and_rejects_ambiguity(self):
        self.assertEqual(money('1.234,56'), money('1,234.56'))
        for value in ('NaN', 'Infinity', '1,234', '1.2.3', '=SUM(A1)'):
            with self.assertRaises(ValueError):
                money(value)

    def test_semicolon_and_malformed_rows(self):
        self.assertEqual('120,50', read_report(b'id;amount\nA-1;120,50\n')[0]['amount'])
        with self.assertRaises(ValueError):
            read_report(b'id,amount\nA-1,10,extra\n')

    def test_runs_and_reviews_survive_restart_and_are_scoped_per_run(self):
        with tempfile.TemporaryDirectory() as folder:
            db = str(Path(folder) / 'records.sqlite3')
            def application():
                app = create_app(review_db=db)
                app.config.update(TESTING=True, SECRET_KEY='fixture')
                return app
            def token(client):
                client.get('/')
                with client.session_transaction() as session:
                    return session['csrf_token']
            app = application()
            client = app.test_client()
            self.assertEqual(400, client.post('/demo').status_code)
            def upload(client):
                return client.post('/conciliar', data={'csrf_token': token(client), 'sales_file': (io.BytesIO(SALES), 'sales.csv'), 'processor_file': (io.BytesIO(PROCESSOR), 'processor.csv')}, follow_redirects=True)
            self.assertEqual(200, upload(client).status_code)
            with client.session_transaction() as session:
                first_run = session['run_id']
            client.post('/revisar/A-1', data={'csrf_token':token(client), 'run_id':first_run, 'review_status':'Resuelta', 'assigned_to':'Ana', 'note':'Verificado'}, follow_redirects=True)
            restarted = application().test_client()
            restored = restarted.get('/')
            self.assertIn(b'Verificado', restored.data)
            self.assertIn(b'Ana', restored.data)
            upload(restarted)
            latest = restarted.get('/')
            self.assertNotIn(b'value="Verificado"', latest.data)
            historical = restarted.get('/?run=' + first_run)
            self.assertIn(b'value="Verificado"', historical.data)


if __name__ == '__main__':
    unittest.main()
