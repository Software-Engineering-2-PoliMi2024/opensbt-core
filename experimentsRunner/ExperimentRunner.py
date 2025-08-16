from . import ExperimentConfig
from lanekeeping import UdacitySimulator
from dataclasses import asdict
from dbInteract import DBinteract
import time
from typing import Tuple, Callable, Dict
from .ExperimentLogger import ExperimentLogger 
from dbInteract import NoDB
import textwrap

class ExperimentRunner:
    def __init__(self, config: ExperimentConfig, db: DBinteract=NoDB(), 
                 logger: ExperimentLogger=ExperimentLogger(), errorRetrayals: int=3):
        self.config = config
        self.db = db
        self.logger = logger
        self.expId = None
        self.errorRetrayals = errorRetrayals

    def run(self) -> Tuple[str, float]:

        if not self.db.connect():
            raise ConnectionError("Unable to connect to dataBase")

        self.expId = self.db.saveScenario(asdict(self.config.scenarioConf))

        self.logger.log(self.expId, f"Experiment started with scenario:\n{self.config.scenarioConf}")

        startTime = time.time()
        for udacityConfig in self.config:
            input = {}
            
            for f in self.config.searchFields:
                input[f.label] = f.get()
            
            for _ in range(self.config.repetition):
                retry_count = 0
                success = False
                while retry_count < self.errorRetrayals and not success:

                    try:
                        result = UdacitySimulator.simulate(simulator_config=udacityConfig)
                        output = asdict(result[0])

                        self.db.saveExperiment(self.expId, input, output)
                        self.logger.log(self.expId, textwrap.dedent(f"Experiment run executed\n\ninput:\n{input}\n\noutput:\n{output}"))

                        success = True

                    except Exception as e:
                        self.logger.log_error(self.expId, f"Error during simulation: {e}")
                        self.db.saveError(self.expId, str(e))

                        retry_count += 1

                if not success:
                    self.logger.log(self.expId, f"Experiment failed after {self.errorRetrayals} retries\nskippin input: {input}")
        
        endTime = time.time()
        expTime = endTime - startTime

        self.db.disconnect()

        self.logger.log(self.expId, f"Experiment finished in {expTime} seconds")

        return self.expId, expTime