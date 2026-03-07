import time
from src.observability.logger import logger


class MetricsTracker:

    def track_latency(self, func):

        def wrapper(*args, **kwargs):

            start = time.time()

            result = func(*args, **kwargs)

            end = time.time()

            latency = end - start

            logger.info(f"Pipeline latency: {latency:.3f} seconds")

            return result

        return wrapper