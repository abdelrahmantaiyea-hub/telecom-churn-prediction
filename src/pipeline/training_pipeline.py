import sys
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class TrainPipeline():
    def run_pipeline(self):
        try:
            # Step 1: Get the data
            ingestion = DataIngestion()
            train_path, test_path = ingestion.initiate_data_ingestion()    

            # Step 2: Clean and Transform 
            transformation = DataTransformation()
            train_arr, test_arr, preprocessor_path = transformation.initiate_data_transformation(train_path, test_path)

            # Step 3: Train the ensemble
            trainer = ModelTrainer()
            score = trainer.initiate_model_trainer(train_arr, test_arr)

            logging.info(f"SUCCESS: Pipeline finished. Final F1: {score}")
            print(f"Final Model Score: {score}")

        except Exception as e:
            raise CustomException(sys, e)    
        
if __name__ == "__main__":
    TrainPipeline().run_pipeline()