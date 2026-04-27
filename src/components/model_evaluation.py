import os
import sys
import pandas as pd
from sklearn.metrics import f1_score
from src.utils import load_object
from src.exception import CustomException
from src.logger import logging

class ModelEvaluation:
    def __init__(self):
        pass

    def initiate_model_evaluation(self, test_df):

        try:
            # Paths to artifacts

            model_path = os.path.join("artifacts", "models", "model_trainer.pkl")
            preprocessor_path = os.path.join("artifacts", "models", "preprocessor.pkl")


            # Load model and preprocessor

            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            target_column_name = "churn"
            x_test = test_df.drop(columns=[target_column_name], axis=1)
            y_test = test_df[target_column_name].map({'Yes': 1, 'No': 0})

            # Transform test data
            x_test_transformed = preprocessor.transform(x_test)

            # Make predictions
            y_pred = model.predict(x_test_transformed)

            # Calculate the F1 Score
            current_f1 = f1_score(y_test, y_pred)

            logging.info(f"Model Evaluation completed. Current F1 Score: {current_f1}")

            threshold = 0.40

            if current_f1 > threshold:
                logging.info("Model passed the evaluation threshold.")
                return True
            else:
                logging.error("Model failed the evaluation threshold. Ingestion stopped.")
                return False

        except Exception as e:
            raise CustomException(e, sys)
        