import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()
env = {}
for key, value in os.environ.items():
	env[key] = value

logger.info('config loaded')