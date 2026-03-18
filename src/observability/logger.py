import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }
        return json.dumps(log_record)

logger = logging.getLogger("llmops")

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log_event(query, risk, response):
    logger.info({
        "event": "fraud_analysis",
        "query": query,
        "risk": risk,
        "response": response
    })