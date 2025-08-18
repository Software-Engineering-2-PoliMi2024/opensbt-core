import logging
from sys import stdout

class ExperimentLogger:
    def __init__(self, handler: logging.Handler=logging.StreamHandler(stdout), level: int=logging.INFO):
        self.logger = logging.getLogger(f"ExperimentLogger_{id(self)}")
        self.logger.handlers.clear()
        self.handler = handler
        self.logger.addHandler(handler)
        self.logger.setLevel(level)

    def log(self, experiment_id: str, message: str):
        self.logger.info(f"experiment({experiment_id}):\n{message}\n")

    def log_error(self, experiment_id: str, message: str):
        self.logger.error(f"experiment({experiment_id}):\n{message}\n")