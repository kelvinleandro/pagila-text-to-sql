import os
import time
from typing import Union
from sqlalchemy import create_engine, Engine, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")


def create_engine_instance(retries: int = 10, delay: int = 10) -> Union[Engine, None]:
    """
    Waits for the database to be ready and returns a SQLAlchemy Engine.
    Retries connection a few times before failing.
    """
    for i in range(retries):
        try:
            print("Attempting to connect to the database...")
            engine: Engine = create_engine(DATABASE_URL, future=True)

            # test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")

            return engine

        except OperationalError as e:
            print(f"Database connection failed: {e}")
            if i < retries - 1:
                print(f"Retrying in {delay} seconds... ({i+1}/{retries})")
                time.sleep(delay)
            else:
                print("❌ Could not connect to the database after several retries.")
                raise


engine = create_engine_instance()
