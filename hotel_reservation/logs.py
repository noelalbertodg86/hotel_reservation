import logging


def get_logger():
    logging.basicConfig(
        format="%(asctime)s : %(name)s : %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    logger = logging.getLogger("Hotel Reservation")
    logger.setLevel("INFO")
    return logger
