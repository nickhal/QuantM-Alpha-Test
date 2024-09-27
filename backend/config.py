import os
from dotenv import load_dotenv
import logging

load_dotenv()

BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')
BINANCE_API_URL = 'https://api.binance.us'

# We'll use in-memory storage for now
KLINE_DATA = {}

class Config:
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://nickhalphide@localhost/kline_data'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=Config.LOG_LEVEL,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('app.log')
            ]
        )

    @staticmethod
    def init_app(app):
        pass