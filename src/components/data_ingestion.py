import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass


from src.exception import CustomException
from src.logger import logging
import pymysql
from dotenv import load_dotenv

load_dotenv()



@dataclass
class DataIngestionConfig:
    """
    Configuration class to define where our artifacts will be stored.
    Using os.path.join ensures this works on Windows and Linux (Production).
    """
    train_data_path: str = os.path.join('artifacts', "data", "train.csv")
    test_data_path: str = os.path.join('artifacts',"data", "test.csv")
    raw_data_path: str = os.path.join('artifacts',"data", "data_full.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Started the Data Ingestion process.")
        try:
            #  Connect to MySQL using credentials from .env
            mydb = mydb = pymysql.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE")
            )
            
            #  Reading from the SQL View 
            query = "SELECT * FROM train_data_final" 
            df = pd.read_sql(query, mydb)
            
            logging.info('Read the dataset as dataframe from MySQL View')

            # Create the 'artifacts' directory 
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            #  Save the full raw data first
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            
            #  The Split: 80/20 with Stratification
            # This ensures both sets have exactly ~28.8% churn
            train_set, test_set = train_test_split(
                df, 
                test_size=0.2, 
                random_state=42, 
                stratify=df['churn'] 
            )

            #  Save the splits to the artifacts folder
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