import logging
from sys import stdout

class ExperimentLogger:
    def __init__(self, handler: logging.Handler=logging.StreamHandler(stdout)):
        self.logger = logging.getLogger(f"ExperimentLogger")
        self.logger.addHandler(handler)
        self.handler = handler

    def log(self, experiment_id: str, message: str):
        self.logger.setLevel(logging.INFO)
        self.logger.info(f"experiment({experiment_id}): \n{message}")

    def log_error(self, experiment_id: str, message: str):
        self.logger.setLevel(logging.ERROR)
        self.logger.error(f"experiment({experiment_id}): \n{message}")