from . import ExperimentConfig
from lanekeeping import UdacitySimulator
from dataclasses import asdict
from dbInteract import DBinteract
import time
from typing import Tuple, Callable, Dict

class ExperimentRunner:
    def __init__(self, config: ExperimentConfig, db: DBinteract=None, log=False):
        self.config = config
        self.db = db
        self.log = log
        self.persist = db is not None
        self.expId = None

    def run(self) -> Tuple[str, float]:
        if self.log:
            print(f"\033[42mrunning experiment for scenario:\n{self.config.scenarioConf}\033[0m")
        if self.persist:

            if not self.db.connect():
                raise ConnectionError("Unable to connect to dataBase")

            print(f"\033[42mdb connected\033[0m")
            self.expId = self.db.saveScenario(asdict(self.config.scenarioConf))

        startTime = time.time()
        for udacityConfig in self.config:
            for _ in range(self.config.repetition):
                input = {}
    
                for f in self.config.searchFields:
                    input[f.label] = f.get()
                
                result = UdacitySimulator.simulate(simulator_config=udacityConfig)
                output = asdict(result[0])
    
                if self.log:
                    print(f"\033[42minput:\n{input}\noutput:\n{output}\033[0m")
                if self.persist:
                    self.db.saveExperiment(self.expId, input, output)
        
        endTime = time.time()
        expTime = endTime - startTime

        if self.persist:
            self.db.disconnect()
        if self.log:
            print(f"\033[42mexperiment id {self.expId}\033[0m")
            print(f"\033[42mexperimentationTime: {expTime}\033[0m")

        return self.expId, expTime