import os
import sys
import pickle
from src.exception import CustomException
from src.logger import logging

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    


def evaluate_models(x_train, y_train, x_test, y_test, models: dict, params: dict):
    
    ## Performs GridSearchCV across multiple models and returns a performance report.
    report = {}
    best_models = {}    
    try:
        logging.info("Started the model Evalutions")
        
        for model_name, model in models.items():
            para = params.get(model_name, {}) # if it didn't find the model name it would just give a default values not an error 

            gs = GridSearchCV(model, para, cv=3, scoring="f1", n_jobs=-1)
            gs.fit(x_train, y_train)

            best_model_obj = gs.best_estimator_
            
            logging.info(f"Best params for {model_name}: {gs.best_params_}")

            y_test_predict = best_model_obj.predict(x_test)
            test_model_score = f1_score(y_test, y_test_predict)

            report[model_name] = test_model_score
            best_models[model_name] = best_model_obj # Store the object!
            
            logging.info(f"Tournament Result: {model_name} scored {test_model_score}")
        return report, best_models  

    except Exception as e:
        raise CustomException(sys, e)    