import logging
from supabase_auth_X_reflex.logging_info import CustomFormatter
import os


def configure_logger():
    logger = logging.getLogger()  # root logger
    log_level = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
    logger.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))
    stream_handler.setFormatter(CustomFormatter())

    logger.addHandler(stream_handler)

    logging.getLogger("watchfiles.main").setLevel(logging.WARNING)


configure_logger()
