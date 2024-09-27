import unittest
from unittest.mock import patch, MagicMock
from backend.data.processing import get_macd, get_rsi

class TestProcessing(unittest.TestCase):

    @patch('backend.data.processing.get_kline_data')
    def test_get_macd(self, mock_get_kline_data):
        # Mock data
        mock_data = [
            {'openTime': 1625097600000, 'close': 100},
            {'openTime': 1625184000000, 'close': 105},
            {'openTime': 1625270400000, 'close': 110},
            {'openTime': 1625356800000, 'close': 115},
        ]
        mock_get_kline_data.return_value = mock_data

        result = get_macd('BTCUSDT', '1d')

        self.assertIsNotNone(result)
        self.assertIn('macd', result)
        self.assertIn('signal', result)
        self.assertIn('histogram', result)

    @patch('backend.data.processing.get_kline_data')
    def test_get_rsi(self, mock_get_kline_data):
        # Mock data
        mock_data = [
            {'openTime': 1625097600000, 'close': 100},
            {'openTime': 1625184000000, 'close': 105},
            {'openTime': 1625270400000, 'close': 110},
            {'openTime': 1625356800000, 'close': 115},
        ]
        mock_get_kline_data.return_value = mock_data

        result = get_rsi('BTCUSDT', '1d')

        self.assertIsNotNone(result)
        self.assertEqual(len(result), len(mock_data))

if __name__ == '__main__':
    unittest.main()