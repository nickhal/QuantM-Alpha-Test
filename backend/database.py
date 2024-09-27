from sqlalchemy import create_engine, Column, Integer, String, Numeric, BigInteger, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from backend.config import Config
import logging

engine = create_engine(Config.DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

logger = logging.getLogger(__name__)

def kline_data_table(suffix):
    return Table(
        f'kline_data_{suffix}',
        Base.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('symbol', String(10), nullable=False),
        Column('interval', String(5), nullable=False),
        Column('open_time', BigInteger, nullable=False),
        Column('open', Numeric(20, 8), nullable=False),
        Column('high', Numeric(20, 8), nullable=False),
        Column('low', Numeric(20, 8), nullable=False),
        Column('close', Numeric(20, 8), nullable=False),
        Column('volume', Numeric(20, 8), nullable=False),
        Column('close_time', BigInteger, nullable=False),
    )

class KLineData(Base):
    __table__ = kline_data_table('default')

    @classmethod
    def create_partition(cls, suffix):
        table_name = f'kline_data_{suffix}'
        if table_name not in Base.metadata.tables:
            table = kline_data_table(suffix)
            return type(f'KLineData_{suffix}', (Base,), {
                '__table__': table,
                '__tablename__': table_name,
            })
        return type(f'KLineData_{suffix}', (Base,), {
            '__table__': Base.metadata.tables[table_name],
            '__tablename__': table_name,
        })

def init_db():
    logger.info("Initializing database...")
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    
    with engine.connect() as connection:
        # Create partitions for different time ranges
        for year in range(2023, 2025):  # Adjust the range as needed
            for quarter in range(1, 5):
                suffix = f"{year}q{quarter}"
                partition_class = KLineData.create_partition(suffix)
                if not inspector.has_table(partition_class.__tablename__):
                    logger.info(f"Creating table: {partition_class.__tablename__}")
                    partition_class.__table__.create(connection)
    
    logger.info("Database initialization complete.")