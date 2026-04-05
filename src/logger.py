import logging
import os
from datetime import datetime


current_file_path = os.path.abspath(__file__) 


src_folder = os.path.dirname(current_file_path)


project_root = os.path.dirname(src_folder)


LOGS_DIR = os.path.join(project_root, "logs")


os.makedirs(LOGS_DIR, exist_ok=True)

#  GENERATE THE FILENAME

LOG_FILE = f"churn_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


#  DEFINE THE FULL FILE PATH
LOG_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILE)

#  CONFIGURE THE "BRAIN"
logging.basicConfig(
    filename=LOG_FILE_PATH,
    
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    
    level=logging.INFO,
)