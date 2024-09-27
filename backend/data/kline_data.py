from sqlalchemy import create_engine, Column, Integer, String, Numeric, BigInteger, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import Config
import pandas as pd
from backend.binance_api import fetch_kline_data as fetch_binance_kline_data

engine = create_engine(Config.DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class KLineData(Base):
    __tablename__ = 'kline_data'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    interval = Column(String(5), nullable=False)
    open_time = Column(BigInteger, nullable=False)
    open = Column(Numeric(20, 8), nullable=False)
    high = Column(Numeric(20, 8), nullable=False)
    low = Column(Numeric(20, 8), nullable=False)
    close = Column(Numeric(20, 8), nullable=False)
    volume = Column(Numeric(20, 8), nullable=False)
    close_time = Column(BigInteger, nullable=False)

def get_kline_data(symbol, interval, start_time, end_time):
    with Session() as session:
        data = session.query(KLineData).filter(
            and_(
                KLineData.symbol == symbol,
                KLineData.interval == interval,
                KLineData.open_time >= start_time,
                KLineData.open_time <= end_time
            )
        ).order_by(KLineData.open_time).all()
        
        return [
            {
                "openTime": int(d.open_time),
                "open": float(d.open),
                "high": float(d.high),
                "low": float(d.low),
                "close": float(d.close),
                "volume": float(d.volume),
                "closeTime": int(d.close_time)
            } for d in data
        ]

def fetch_and_store_kline_data(symbol, interval, start_time, end_time):
    data = fetch_binance_kline_data(symbol, interval, start_time, end_time)
    with Session() as session:
        for item in data:
            kline = KLineData(
                symbol=symbol,
                interval=interval,
                open_time=item['openTime'],
                open=item['open'],
                high=item['high'],
                low=item['low'],
                close=item['close'],
                volume=item['volume'],
                close_time=item['closeTime']
            )
            session.add(kline)
        session.commit()
    return data

def get_macd_data(symbol, interval):
    # Implement MACD calculation here
    pass

def get_rsi_data(symbol, interval):
    # Implement RSI calculation here
    pass