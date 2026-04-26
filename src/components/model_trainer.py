import os 
import sys 
import numpy as np
import pandas as pd
from dataclasses import dataclass


from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score, 
    confusion_matrix, 
    classification_report, 
    precision_score, 
    recall_score, 
    f1_score, 
    roc_auc_score,
    roc_curve,
    precision_recall_curve
)

from src.logger import logging
from src.exception import CustomException
from src.utils import evaluate_models, save_object

@dataclass

class ModelTrainerConfig:
    model_trainer_obj_file_path: str= os.path.join("artifacts","models", "model_trainer.pkl")



class ModelTrainer:
    def __init__(self):
        
        try:
            self.model_trainer_config: ModelTrainerConfig = ModelTrainerConfig()
            os.makedirs(os.path.dirname(self.model_trainer_config.model_trainer_obj_file_path), exist_ok=True)
        
        except Exception as e:
            raise CustomException(sys, e)        


    def initiate_model_trainer(self, train_array, test_array):
        
        try:
            logging.info("Splitting training and test input data")
            
            x_train, y_train = train_array[:,:-1], train_array[:,-1]      
            x_test, y_test = test_array[:,:-1], test_array[:,-1]     

            models = {
                "Random Forest": RandomForestClassifier(
                    class_weight='balanced_subsample', # Fixed for imbalance
                    random_state=42,                   # Fixed for reproducibility
                    n_jobs=-1
                ),
                "XGBoost": XGBClassifier(
                    scale_pos_weight=2.44,             # Fixed based on ~29% churn math
                    random_state=42,
                    eval_metric='logloss'
                )}
            params = {
                "Random Forest": {
                    "n_estimators": [100, 200, 300],    # Testing small, medium, large forest
                    "max_depth": [10, 20, None],         # Testing controlled vs. deep growth
                    "criterion": ['gini', 'entropy']
                },
                "XGBoost": {
                    "learning_rate": [0.1, 0.01],
                    "n_estimators": [100, 200],
                    "max_depth": [3, 5, 7],
                    "subsample": [0.8, 1.0]
                }}
            
            model_report, best_models_found = evaluate_models(x_train, y_train, x_test, y_test, models, params)

            best_model_score = max(sorted(model_report.values()))

            if best_model_score < 0.4:
                logging.warning(f"Best model score {best_model_score} is below the 0.4 threshold!")
                raise CustomException("Model performance insufficient for business deployment.")

            logging.info(f"Tournament Winner passed the business threshold with a score of: {best_model_score}")

            tuned_rf = best_models_found["Random Forest"]
            tuned_xgb = best_models_found["XGBoost"]

            # create the ensemble model

            ensemble_model = VotingClassifier(
                estimators=
                [("rf", tuned_rf),
                ("xgb", tuned_xgb)],
                voting= "soft"
            )           
            logging.info("Assembling and fitting the final Soft-Voting Ensemble.")

            ensemble_model.fit(x_train, y_train)

            save_object(file_path=self.model_trainer_config.model_trainer_obj_file_path,
                        obj=ensemble_model)
            
            y_pred = ensemble_model.predict(x_test)
            ensemble_score = f1_score(y_test, y_pred)
            
            logging.info(f"Ensemble Score on Test Data: {ensemble_score}")
            
            return ensemble_score
        except Exception as e:
            raise CustomException(sys, e)
