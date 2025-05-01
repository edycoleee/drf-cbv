# myproject/utils/logging_decorator.py

import logging
import functools

logger = logging.getLogger('myproject')  # sesuaikan dengan nama logger di settings.py

def log_method(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"➡️  Masuk ke method: {func.__qualname__}")
        logger.debug(f"   ┣ args: {args}")
        logger.debug(f"   ┗ kwargs: {kwargs}")

        try:
            result = func(*args, **kwargs)
            logger.info(f"⬅️  Keluar dari method: {func.__qualname__}")
            logger.debug(f"   ┗ Hasil: {result}")
            return result
        except Exception as e:
            logger.error(f"💥 Error di method: {func.__qualname__} → {e}")
            raise
    return wrapper
