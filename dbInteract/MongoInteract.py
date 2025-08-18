from pymongo.mongo_client import MongoClient
from bson import ObjectId
from .DBinteract import DBinteract
from . import dbLabels
import threading
import queue
from typing import Dict, List
import time
import orjson

class MongoInteract(DBinteract):
    def __init__(self, dbUri: str):
        self.dbUri = dbUri
        self.client = None
        self.db = None
        self.experimentToSave = queue.Queue()
        self.expSaverRun = True

        threading.Thread(
            target=self._persistExperiment,
            args=()
        ).start()

    def connect(self):
        self.client = MongoClient(self.dbUri)
        try:
            self.client.admin.command('ping')
            self.db = self.client[dbLabels.DB_NAME]

            return True
        except Exception as e:
            return False                  

    def saveScenario(self, scenarioConf: Dict) -> str:
        result = self.db[dbLabels.SCENARIO_coll].insert_one(scenarioConf)
        return result.inserted_id

    def saveExperiment(self, experimentId, input: Dict, output: Dict) -> None:
        exp = {"scenario": experimentId,
               "in": orjson.loads(orjson.dumps(input, option=orjson.OPT_SERIALIZE_NUMPY)), 
               "out": orjson.loads(orjson.dumps(output, option=orjson.OPT_SERIALIZE_NUMPY))
            }
        self.experimentToSave.put(exp)

    def saveError(self, experimentId, input: Dict, error: str) -> None:
        error = {"scenario": experimentId, 
                 "in": orjson.loads(orjson.dumps(input, option=orjson.OPT_SERIALIZE_NUMPY)),
                 "error": error
                }
        self.db[dbLabels.EXP_ERR_coll].insert_one(error)
        return

    def _persistExperiment(self, batch=1, timeSleep=1):
        while self.expSaverRun or not self.experimentToSave.empty():
            
            if self.experimentToSave.qsize() < batch and self.expSaverRun:
                time.sleep(timeSleep)
                continue

            items = [self.experimentToSave.get() for _ in range(min(batch, self.experimentToSave.qsize()))]
            
            self.db[dbLabels.EXP_RUN_coll].insert_many(items)

    def extractScenario(self, id: str) -> Dict:
        id = ObjectId(id) 
        scenario = self.db[dbLabels.SCENARIO_coll].find_one({"_id": id})
        if scenario is not None:
            return scenario
        return {}

    def extractExperiment(self, id: str) -> Dict:
        id = ObjectId(id)
        experiment = self.db[dbLabels.EXP_RUN_coll].find_one({"_id": id})
        if experiment is not None:
            return experiment
        return {}

    def extractExperimentsByScenario(self, scenarioId: str) -> List[Dict]:
        scenarioId = ObjectId(scenarioId)
        experiments = list(self.db[dbLabels.EXP_RUN_coll].find({"scenario": scenarioId}))
        return experiments

    def disconnect(self):
        self.expSaverRun = False
        self.client.close()