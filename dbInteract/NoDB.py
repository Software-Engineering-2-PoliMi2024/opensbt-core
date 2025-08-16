from .DBinteract import DBinteract
from typing import Dict, List

class NoDB(DBinteract):
    def __init__(self):
        """NoDB is a placeholder for when no database interaction is needed."""

    def connect(self) -> bool:
        return True
    
    def saveScenario(self, scenarioConf: Dict) -> str:
        return "NoDB - scenario not persisted"
    
    def saveExperiment(self, experimentId, input: Dict, output: Dict) -> None:
        return

    def saveError(self, experimentId, error: str) -> None:
        return
    
    def extractScenario(self, id) -> Dict:
        raise NotImplementedError("NoDB does not support scenario extraction")

    def extractExperiment(self, id) -> Dict:
        raise NotImplementedError("NoDB does not support experiment extraction")
    
    def extractExperimentsByScenario(self, scenarioId) -> List[Dict]:
        raise NotImplementedError("NoDB does not support experiments extraction by scenario")

    def disconnect(self) -> None:
        return