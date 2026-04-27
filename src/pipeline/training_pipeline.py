import sys
import pandas as pd 
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher



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
            logging.info(f"Training complete. F1: {score}")

            # Step 4: Model Evaluation 

            test_df = pd.read_csv(test_path)
            evaluator = ModelEvaluation()
            is_passed = evaluator.initiate_model_evaluation(test_df)

            # Step 5: Model Pusher

            if is_passed:
                pusher = ModelPusher()
                pusher.initiate_model_push()
                logging.info("SUCCESS: Model pushed to saved_models.")
                print(f"Final Model Score: {score} - DEPLOYED.")
            else:
                logging.warning("Model did not meet evaluation threshold.")
                print("Model failed evaluation. It will NOT be pushed to production.")

            logging.info(f"SUCCESS: Pipeline finished. Final F1: {score}")
            print(f"Final Model Score: {score}")

        except Exception as e:
            raise CustomException(e, sys)    
        
if __name__ == "__main__":
    TrainPipeline().run_pipeline()