import logging
from contextvars import ContextVar
import time
import requests

from utils.variables import ENV, LOKI_URL
# ContextVar to store the trace ID for the current context
trace_id_var = ContextVar("trace_id", default="")

# Loki configuration
LOKI_URL = LOKI_URL
ENV = ENV


class CustomFormatter(logging.Formatter):
    def format(self, record):
        trace_id = trace_id_var.get()
        record.trace_id = trace_id
        return super().format(record)


class SyncLokiHandler(logging.Handler):
    def __init__(self, url, labels=None):
        super().__init__()
        self.url = url
        self.labels = labels if labels else {}

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.send_log(log_entry)
        except Exception as e:
            print(f"Failed to send log to Loki: {e}")

    def send_log(self, log_entry):
        payload = {
            "streams": [
                {
                    "stream": self.labels,
                    "values": [[str(int(time.time() * 1e9)), log_entry]]
                }
            ]
        }
        headers = {'Content-type': 'application/json'}
        response = requests.post(self.url, json=payload, headers=headers)
        response.raise_for_status()


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Console handler (CloudWatch will capture this)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(trace_id)s - %(message)s'))

    # Loki handler
    loki_handler = SyncLokiHandler(
        url=LOKI_URL,
        labels={"service": "lambda-function", "env": ENV}
    )
    loki_handler.setLevel(logging.INFO)
    loki_handler.setFormatter(CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(trace_id)s - %(message)s'))

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(loki_handler)

    return logger


# Create a logger instance
logger = get_logger("lambda_function")
