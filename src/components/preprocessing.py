import numpy as np 
import pandas as pd 
import sys

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

def cap_outliers(X):
    try:
        X_copy = np.copy(X) # to not override the previous data
        # Calculate limits for each column (axis=0)
        lower_limit = np.percentile(X_copy, 1, axis=0)
        upper_limit = np.percentile(X_copy, 99, axis=0) 
        return np.clip(X_copy, a_min=lower_limit, a_max=upper_limit)       
    except Exception as e:
        raise CustomException(e, sys)
    

def handle_handset_price(X):
    try:
        
        df = pd.DataFrame(X)
        
      # run throught lying zeros and converts the object ones
        for col in df.columns:
            # Convert to numeric, turn 'unknown' to NaN, then NaN to 0
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        return df.to_numpy()
    except Exception as e:
        raise CustomException(e, sys)  