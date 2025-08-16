from .DBinteract import DBinteract
from typing import Dict, List

class NoDB(DBinteract):
    def __init__(self):
        return
    
    def connect(self) -> bool:
        return True
    
    def saveScenario(self, scenarioConf: Dict) -> str:
        return "NoDB - scenario not saved"
    
    def saveExperiment(self, experimentId, input: Dict, output: Dict):
        return "NoDB - scenario not saved"
    
    def extractScenario(self, id) -> Dict:
        raise NotImplementedError("NoDB does not support scenario extraction")

    def extractExperiment(self, id) -> Dict:
        raise NotImplementedError("NoDB does not support experiment extraction")
    
    def extractExperimentsByScenario(self, scenarioId) -> List[Dict]:
        raise NotImplementedError("NoDB does not support experiments extraction by scenario")

    def disconnect(self) -> None:
        return