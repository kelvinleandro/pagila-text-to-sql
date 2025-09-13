import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from langchain_community.utilities import SQLDatabase
from app.core.config import settings
from typing import Union


def create_instance() -> Union[SQLDatabase, None]:
    """
    Waits for the database to be ready and returns a LangChain SQLDatabase instance.
    """
    retries = 10
    delay = 10

    for i in range(retries):
        try:
            print("Attempting to connect to the database...")
            engine = create_engine(settings.DATABASE_URL)
            engine.connect()

            print("✅ Database connection successful!")
            return SQLDatabase(engine=engine)

        except OperationalError as e:
            print(f"Database connection failed: {e}")
            if i < retries - 1:
                print(f"Retrying in {delay} seconds... ({i+1}/{retries})")
                time.sleep(delay)
            else:
                print("❌ Could not connect to the database after several retries.")
                raise


db_instance = create_instance()
