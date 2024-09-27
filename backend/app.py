from flask import Flask
from flask_cors import CORS
from backend.routes import api
from backend.config import Config
from backend.database import engine, Base, KLineData
from sqlalchemy import inspect
import logging

logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    Config.setup_logging()
    
    app.register_blueprint(api, url_prefix='/api')
    
    # Check if the database exists and has tables
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    if not existing_tables:
        logger.info("Database is empty. Initializing tables...")
        with app.app_context():
            Base.metadata.create_all(engine)
    else:
        logger.info("Database already initialized. Checking for missing tables...")
    
    # Ensure all partition tables are created
    with engine.connect() as connection:
        for year in range(2023, 2025):  # Adjust the range as needed
            for quarter in range(1, 5):
                suffix = f"{year}q{quarter}"
                table_name = f'kline_data_{suffix}'
                if table_name not in existing_tables:
                    logger.info(f"Creating missing table: {table_name}")
                    partition_class = KLineData.create_partition(suffix)
                    partition_class.__table__.create(connection)
    
    logger.info("Database initialization and table check complete.")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)