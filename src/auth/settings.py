import os

from dotenv import load_dotenv
import logging

load_dotenv()
DATABASE_URI= os.environ.get("DATABASE_URI")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

# Configure the basic logger
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log message format
    handlers=[
        logging.StreamHandler()  # Output logs to the terminal (stdout)
    ]
)

# Example usage of the logger
logger = logging.getLogger(__name__)