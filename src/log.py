import logging
import logging.handlers

def setup_logger(name, logfile='log.txt'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even DEBUG messages
    fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=1000000, backupCount=5)
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(fh_formatter)

    logger.addHandler(fh)
    return logger
