import os
import sys
import pandas as pd
import numpy as np
import json

from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import FunctionTransformer

from src.components.preprocessing import cap_outliers, handle_handset_price
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass

class DataTransformationConfig:

    preprocessor_obj_file_path: str = os.path.join("artifacts","models", "preprocessor.pkl")
    train_array_file_path: str = os.path.join("artifacts", "data", "train_array.npy")
    test_array_file_path: str = os.path.join("artifacts", "data", "test_array.npy")
   
 
    
class DataTransformation:
    
    def __init__(self):
        
        try:
        
            self.transformation_config: DataTransformationConfig  = DataTransformationConfig()   

        except Exception as e:
            raise CustomException(e, sys)    
        

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)    
  

        

    def get_data_transformer_object(self):
        """
        Creates and returns a data transformer object for the data, 
        including Handling lyign Zeros and Nulls,type adjustments , Handling Outliers, dummy variables mapping,
        and feature scaling.
        """

        logging.info("Entered the Data tranformer object method.")

        try:

            logging.info("Starting Pipeline construction with 4 specific lanes")

            lying_zero_columns = ['AgeHH1', 'IncomeGroup', 'HandsetPrice']


            extreme_messy_columns = ['MonthlyRevenue', 'OverageMinutes', 'PercChangeRevenues', 
               'MonthlyMinutes', 'PercChangeMinutes', 'RoamingCalls']
            
             # Extreme variance but almost zero nulls

            extreme_clean_columns = ["CurrentEquipmentDays"]
            
            stable_columns = [ 'MonthsInService','DroppedCalls', 
                                      'BlockedCalls', 'CustomerCareCalls', "TotalRecurringCharge", "ReferralsMadeBySubscriber"]
            
            categorical_columns = ["HandsetRefurbished", "HandsetWebCapable", "CreditRating", "Occupation"]
            
            logging.info("Transformers Initialized")

            # LANE 1: THE LYING ZEROS (Standard Scaling + 0-Imputation)

            lying_zero_pipeline = Pipeline(steps=[
                ("handler" , FunctionTransformer(handle_handset_price, feature_names_out='one-to-one')),
                ("imputer", SimpleImputer(strategy="median", missing_values=0, add_indicator=True)),
                ("scaler", StandardScaler())
                ])
            
            # LANE 2: EXTREME NUMERIC OUTLIERS (Robust Scaling + Capping)
            
            extreme_messy_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                ("capper", FunctionTransformer(cap_outliers, feature_names_out='one-to-one')),
                ("scaler", RobustScaler())
            ])

            # LANE 3: EXTREME CLEAN (Capping + Robust + NO Indicator)

            extreme_clean_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median", add_indicator=False)),
                ("capper", FunctionTransformer(cap_outliers, feature_names_out='one-to-one')),
                ("scaler", RobustScaler())
            ])


            # LANE 4: STABLE NUMERIC OUTLIERS (Standard Scaling)
            
            stable_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                ("scaler", StandardScaler())
            ])

            # LANE 5: CATEGORICAL (Dummies)
            
            cat_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder", OneHotEncoder(handle_unknown='ignore')),
                ("scaler", StandardScaler(with_mean=False))
            ])
            logging.info("Assembling individual pipelines into ColumnTransformer.")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("lying_zero_lane", lying_zero_pipeline, lying_zero_columns),
                    ("extreme_messy_lane", extreme_messy_pipeline, extreme_messy_columns),
                    ("extreme_clean_lane", extreme_clean_pipeline, extreme_clean_columns),
                    ("stable_messy_lane", stable_pipeline, stable_columns),
                    ("categorical_lane", cat_pipeline, categorical_columns)
                ],
                remainder="drop"
            )
            logging.info("ColumnTransformer object created successfully.")

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, train_path, test_path):

        """
        Initiates the data transformation component for the pipeline.
        """
        try:
            logging.info("Data Transformation Started !!!")

            # 1. Load the data using your method

            train_df = self.read_data(train_path)
            test_df = self.read_data(test_path)

            logging.info("Reading train and test data completed")

            # 2. Obtain the Preprocessing "Brain" we built

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "churn"

            target_map = {'Yes': 1, 'No': 0}

            logging.info("Mapping target column to binary integers")
            
            train_df[target_column_name] = train_df[target_column_name].map(target_map)
            test_df[target_column_name] = test_df[target_column_name].map(target_map)
            
            # 3. Separate Features (X) and Target (y)
            
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataframes.")

            # 4. THE EXECUTION
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)

            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)


            final_feature_names = preprocessing_obj.get_feature_names_out()

            names_path = os.path.join("artifacts", "data", "feature_names.json")
            
            with open(names_path, 'w') as f:
                json.dump(list(final_feature_names), f)
            
            # 5. Combine X and y into a single array for the Model Trainer

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            
            logging.info("Saving train and test arrays to disk...")
            
            
            np.save(self.transformation_config.train_array_file_path, train_arr)
            np.save(self.transformation_config.test_array_file_path, test_arr)

            # 6. SAVE THE MACHINE (The .pkl file)
            save_object(
                file_path=self.transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            # Return the ready arrays and the path to the saved pkl
            return (
                train_arr,
                test_arr,
                self.transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)        

