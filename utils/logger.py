import sys
import logging

LOG = logging.getLogger("Jarvis")
LOG.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(message)s]')
handler.setFormatter(formatter)

LOG.addHandler(handler)