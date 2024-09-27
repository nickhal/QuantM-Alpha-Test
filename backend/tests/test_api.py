import unittest
from backend.app import create_app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_kline_endpoint(self):
        response = self.client.get('/api/kline?symbol=BTCUSDT&interval=1h')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_macd_endpoint(self):
        response = self.client.get('/api/macd?symbol=BTCUSDT&interval=1h')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('macd', data)
        self.assertIn('signal', data)
        self.assertIn('histogram', data)

    def test_rsi_endpoint(self):
        response = self.client.get('/api/rsi?symbol=BTCUSDT&interval=1h')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_symbols_endpoint(self):
        response = self.client.get('/api/symbols')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertIn('BTCUSDT', data)

if __name__ == '__main__':
    unittest.main()