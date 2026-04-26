import os
import sys
import numpy as np
from src.components.model_trainer import ModelTrainer
from src.logger import logging

def test_component():
    try:
        logging.info("Starting Independent Component Test for ModelTrainer...")

        # 1. Paths to your transformed data (Adjust if your filenames are different)
        train_array_path = os.path.join("artifacts", "data", "train_array.npy")
        test_array_path = os.path.join("artifacts", "data", "test_array.npy")

        # 2. Check if the files actually exist before trying to load
        if not os.path.exists(train_array_path) or not os.path.exists(test_array_path):
            print("❌ Error: Transformed .npy files not found in artifacts folder.")
            print("Make sure you have run your DataTransformation component first!")
            return

        # 3. Load the transformed arrays
        logging.info("Loading transformed arrays from artifacts...")
        train_arr = np.load(train_array_path)
        test_arr = np.load(test_array_path)

        # 4. Initialize and Run the Model Trainer
        trainer = ModelTrainer()
        logging.info("Calling initiate_model_trainer...")
        
        # This will run the GridSearch tournament and the Ensemble fitting
        model_score = trainer.initiate_model_trainer(train_arr, test_arr)

        print(f"\n✅ SUCCESS!")
        print(f"Final Ensemble Score: {model_score}")
        print(f"Model saved to: {trainer.model_trainer_config.model_trainer_obj_file_path}")

    except Exception as e:
        print(f"❌ Component Test Failed: {e}")

if __name__ == "__main__":
    test_component()