import logging

logging.basicConfig(filename='herzog.log', level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def getlogger(name) :
    logger = logging.getLogger(name)
    # logger.addHandler(ch)
    return logger

logger = logging.getLogger('herzog')
