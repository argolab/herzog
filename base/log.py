import logging
from .app import app

logging.basicConfig(filename='herzog.log', level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
app.logger.addHandler(ch)

def getlogger(name) :
    logger = logging.getLogger(name)
    logger.addHandler(ch)
    return logger

logger = logging.getLogger('herzog')
