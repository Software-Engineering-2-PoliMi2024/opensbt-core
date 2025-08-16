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
    def __init__(self, config: ExperimentConfig, db: DBinteract=NoDB, logger: ExperimentLogger=ExperimentLogger()):
        self.config = config
        self.db = db
        self.logger = logger
        self.expId = None

    def run(self) -> Tuple[str, float]:

        if not self.db.connect():
            raise ConnectionError("Unable to connect to dataBase")

        self.expId = self.db.saveScenario(asdict(self.config.scenarioConf))

        self.logger.log(self.expId, textwrap.dedent(f"Experiment started with scenario: \n\
                                   {self.config.scenarioConf}"))

        startTime = time.time()
        for udacityConfig in self.config:
            for _ in range(self.config.repetition):
                input = {}
    
                for f in self.config.searchFields:
                    input[f.label] = f.get()
                
                result = UdacitySimulator.simulate(simulator_config=udacityConfig)
                output = asdict(result[0])
    
                self.logger.log(self.expId, textwrap.dedent(f"Experiment run executed\n\
                                           input:\n\
                                           {input}\n\
                                           output:\n\
                                           {output}"))
                
                self.db.saveExperiment(self.expId, input, output)
        
        endTime = time.time()
        expTime = endTime - startTime

        self.db.disconnect()

        self.logger.log(self.expId, f"Experiment finished in {expTime} seconds")

        return self.expId, expTime