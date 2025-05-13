import logging
import os
from datetime import datetime


# Basic logger settings
def setup_logger():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Set log format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            # Save logs to file
            logging.FileHandler(
                f'logs/shop_{datetime.now().strftime("%Y-%m-%d")}.log',
                encoding='utf-8'
            ),
            # Display logs in console
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('shop')

# Create an instance of the logger
logger = setup_logger()
