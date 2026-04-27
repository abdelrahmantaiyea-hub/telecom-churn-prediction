import os
import sys
import shutil
from src.exception import CustomException
from src.logger import logging

class ModelPusher:
    def __init__(self):
        
        self.saved_model_path = os.path.join("saved_models")

    def initiate_model_push(self):
        try:

            logging.info("Initiating model pusher...")

            source_model = os.path.join("artifacts", "models", "model_trainer.pkl")
            source_preprocessor = os.path.join("artifacts", "models", "preprocessor.pkl")

            # Destination
            os.makedirs(self.saved_model_path, exist_ok=True)

            shutil.copy(source_model, self.saved_model_path)
            shutil.copy(source_preprocessor, self.saved_model_path)

            logging.info(f"Model and Preprocessor pushed to {self.saved_model_path}")

            return self.saved_model_path

        except Exception as e:
            raise CustomException(e, sys)        

