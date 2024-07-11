import os
import sys
import logging
from datetime import datetime

# Define log file name and path
LOG_FILE = datetime.now().strftime('%m_%d_%y_%H_%M') + '.log'
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# Configure logging
logging.basicConfig(
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)

# Additional console logging configuration
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(levelname)-8s %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)

if __name__ == "__main__":
    MESSAGE = "Logging is started..."
    logging.info(MESSAGE)
