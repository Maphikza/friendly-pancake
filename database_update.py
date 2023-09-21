from sqlalchemy import create_engine, update, MetaData
from sqlalchemy.orm import sessionmaker
import os
from log_config import logger

# Create a PostgreSQL database engine
db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url)

# Reflect existing database into a new model
metadata = MetaData()
metadata.reflect(bind=engine)

# Get Table
service_fees = metadata.tables['service_fees']

# Create a SQLAlchemy session
Session = sessionmaker(bind=engine)


def update_exchange_rate(updated_rate: float) -> bool:
    if isinstance(updated_rate, float):
        session = Session()

        # Specify the unique identifier for the row you want to update
        target_id = os.environ.get('SERVICE_ID')

        # Create the update statement
        update_statement = (
            update(service_fees)
            .where(service_fees.c.id == target_id)
            .values(aud_conversion_rate=updated_rate)
        )

        # Execute the update statement and commit changes
        session.execute(update_statement)
        session.commit()

        # Close the session when you're done
        session.close()

        logger.info("Exchange Rate updated")
        return True
    else:
        logger.error("The updated rate was not a float data type. So it is not updated.")
        return False
