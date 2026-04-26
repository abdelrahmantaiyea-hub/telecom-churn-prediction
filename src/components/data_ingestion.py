import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "data", "train.csv")
    test_data_path: str = os.path.join('artifacts', "data", "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data", "data_full.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Started the Data Ingestion process.")
        try:
            # Constructing the SQLAlchemy connection URI
            conn_uri = (
                f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
                f"{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/"
                f"{os.getenv('MYSQL_DATABASE')}"
            )
            
            # Creating the engine for modern database interaction
            engine = create_engine(conn_uri)
            
            query = "SELECT * FROM train_data_final" 
            
            # Using context manager to ensure connection is properly closed
            with engine.connect() as connection:
                df = pd.read_sql(query, connection)
            
            logging.info('Read the dataset as dataframe via SQLAlchemy Engine')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            
            train_set, test_set = train_test_split(
                df, 
                test_size=0.2, 
                random_state=42, 
                stratify=df['churn'] 
            )

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()