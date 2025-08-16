from abc import ABC, abstractmethod
from typing import Dict, List

class DBinteract(ABC):
    @abstractmethod
    def __init__():
        pass

    @abstractmethod
    def connect(self) -> bool:
        """Establish a connection to the database and return True if successful."""
        print("must be implemented in subclass")
        
    def saveScenario(self, scenarioConf: Dict) -> str:
        """Save the scenario configuration to the database and return its ID."""
        print("must be implemented in subclass")
        return ""
    
    def saveExperiment(self, experimentId, input: Dict, output: Dict) -> None:
        """Save the experiment data to the database and return its ID."""
        print("must be implemented in subclass")
        return ""
    
    def saveError(self, experimentId, error: str) -> None:
        """Save an error that occurred during the experiment to the database."""
        print("must be implemented in subclass")
        return
    
    def extractScenario(self, id) -> Dict:
        """Extract a scenario configuration from the database by its ID."""
        print("must be implemented in subclass")
        return {}

    def extractExperiment(self, id) -> Dict:
        """Extract an experiment data from the database by its ID."""
        print("must be implemented in subclass")
        return {}
    
    def extractExperimentsByScenario(self, scenarioId) -> List[Dict]:
        """Extract all experiments associated with a specific scenario ID."""
        print("must be implemented in subclass")
        return {}

    def disconnect(self)-> None:
        """Disconnect from the database."""
        print("must be implemented in subclass")
        return