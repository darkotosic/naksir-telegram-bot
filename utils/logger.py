import logging
import os

def get_logger(name: str = "naksir"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Izbegni duplo dodavanje handlera
    if not logger.handlers:
        # Formatter
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] - %(message)s", "%Y-%m-%d %H:%M:%S"
        )

        # Stream (terminal) handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # File handler
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler("logs/naksir.log", mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
