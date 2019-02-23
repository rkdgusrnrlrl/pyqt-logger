import logging

logger = logging.getLogger("pyqt-logger")
handler = logging.FileHandler('pyqt_logger.log')
logger.addHandler(handler)
logging.basicConfig(level=logging.INFO)
