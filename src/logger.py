import os
import sys
import logging
from datetime import datetime

LOG_FILE =f"{datetime.now().strftime('%m_%d_%y_%H_%M')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)

if __name__=="__main__":
    MESSAGE = "Logging is started..."
    logging.info(msg=MESSAGE)