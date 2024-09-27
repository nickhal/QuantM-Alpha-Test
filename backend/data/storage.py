from backend.database import Session, KLineData, Base
from sqlalchemy import and_
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_partition_suffix(timestamp):
    date = datetime.fromtimestamp(timestamp / 1000)
    return f"{date.year}q{(date.month - 1) // 3 + 1}"

def save_kline_data(symbol, interval, data):
    with Session() as session:
        for item in data:
            try:
                suffix = get_partition_suffix(item['openTime'])
                PartitionClass = KLineData.create_partition(suffix)
                kline = PartitionClass(
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
            except Exception as e:
                logger.error(f"Error saving kline data: {e}")
                logger.error(f"Problematic item: {item}")
        try:
            session.commit()
        except Exception as e:
            logger.error(f"Error committing to database: {e}")
            session.rollback()

def get_kline_data(symbol, interval, start_time, end_time):
    with Session() as session:
        start_suffix = get_partition_suffix(start_time)
        end_suffix = get_partition_suffix(end_time)
        
        data = []
        current_suffix = start_suffix
        while current_suffix <= end_suffix:
            PartitionClass = KLineData.create_partition(current_suffix)
            query = session.query(PartitionClass).filter(
                and_(
                    PartitionClass.symbol == symbol,
                    PartitionClass.interval == interval,
                    PartitionClass.open_time >= start_time,
                    PartitionClass.open_time <= end_time
                )
            ).order_by(PartitionClass.open_time)
            
            data.extend(query.all())
            
            # Move to the next quarter
            year, quarter = map(int, current_suffix.split('q'))
            if quarter == 4:
                year += 1
                quarter = 1
            else:
                quarter += 1
            current_suffix = f"{year}q{quarter}"
        
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