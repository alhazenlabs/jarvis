import sys
import logging
from utils.constants import Constants

LOG = logging.getLogger("Jarvis")
LOG.setLevel(Constants.LOG_LEVEL)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(Constants.LOG_LEVEL)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(message)s]')
handler.setFormatter(formatter)

LOG.addHandler(handler)
