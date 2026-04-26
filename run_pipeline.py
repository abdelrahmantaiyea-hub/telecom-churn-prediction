# run_pipeline.py
from src.components.data_transformation import DataTransformation
import os

if __name__ == "__main__":
    train_path = os.path.join("artifacts", "data", "train.csv")
    test_path = os.path.join("artifacts", "data", "test.csv")

    # This trigger ensures the pickle saves the address as:
    # "src.components.data_transformation.handle_handset_price"
    # NOT "__main__.handle_handset_price"
    transformer = DataTransformation()
    train_arr, test_arr, pre_path = transformer.initiate_data_transformation(train_path, test_path)
    
    print(f"✅ Transformation Complete! Artifacts saved.")
    print(f"✅ You can now open the notebook and use the preprocessor without errors.")