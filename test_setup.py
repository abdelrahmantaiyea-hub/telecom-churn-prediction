import sys
from src.logger import logging
from src.exception import CustomException

def test_the_infrastructure():
    try:
        logging.info("Starting the final infrastructure test...")
        
        # This will trigger a ZeroDivisionError
        result = 1/0
        
    except Exception as e:
        # We catch the raw error 'e' and wrap it in our 'CustomException'
        # We pass 'sys' so it can access the internal traceback
        logging.error("A math error occurred. Triggering CustomException...")
        raise CustomException(e, sys)

if __name__ == "__main__":
    test_the_infrastructure()