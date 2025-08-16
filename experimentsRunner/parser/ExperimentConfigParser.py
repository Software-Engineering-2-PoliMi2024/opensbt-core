from typing import Callable, Dict, Tuple, List
from lanekeeping.udacity.UdacitySimulatorConfig import UdacitySimulatorConfig
from ..ExperimentConfig import ExperimentConfig
from . import fileLabels
from ..SearchField import SearchField
import re
import orjson

class ExperimentConfigParser:
    def parse(self, filePath: str, source: Callable[[str], Dict] = None) -> ExperimentConfig:
        if source is None:
            source = lambda f: self._loadJson(f)

        conf = source(filePath)

        scenarioConf = self._loadScenario(conf)
        searchFields = self._loadSearchFields(conf, scenarioConf)
        repetition = self._loadRepetiotion(conf)    
        

        return ExperimentConfig(scenarioConf, searchFields, repetition)

    def _loadRepetiotion(self, config: Dict) -> int:
        """load the times each experiment should be repeated"""
        
        repetition = config.get(fileLabels.REPETITION)
        
        if repetition is None or not isinstance(repetition, int) or repetition <= 0:
            repetition = 1
        
        return repetition

    def _loadScenario(self, config: Dict) -> UdacitySimulatorConfig:
        """load the scenario configuration from a configuration dictionary"""
        
        assert fileLabels.SCENARIO in config, f"Missing '{fileLabels.SCENARIO}' in configuration"
        return UdacitySimulatorConfig.fromDict(config[fileLabels.SCENARIO])

    def _loadSearchFields(self, config: Dict, scenarioConf: UdacitySimulatorConfig) -> List[SearchField]:
        """load the search fields from a configuration dictionary"""
        
        searchFields = []
        parse_handlers= [((lambda l: self._checkIfCallectionLabel(l)),
                           lambda f, config: self._parseCollection(f, config))
                        ]
        loadedSearchConf = config.get(fileLabels.SEARCH_PAR)

        if loadedSearchConf is not None:
            finalSearchConf: List[Dict] = []
            updateConfigs: List[Callable] = []
            
            for field in loadedSearchConf:
                label = field[fileLabels.FIELD_LABEL]

                if not self._validSearchFieldLabel(label):
                    raise f"'{label}' is not correctly formatted"
                
                for k, v in parse_handlers:
                    if(k(label)): 
                        parsedField, updateMethod = v(field, scenarioConf)
                        finalSearchConf += parsedField
                        updateConfigs += updateMethod
                    else:
                        finalSearchConf += [field]
                        updateConfigs += [(lambda value, cLbl=label: setattr(scenarioConf, cLbl, value))]
                    
            assert len(finalSearchConf) == len(updateConfigs)

            searchFields = [SearchField.fromDict(field, method) for field, method in list(zip(finalSearchConf, updateConfigs))]

        return searchFields

    def _loadJson(self, filePath: str) -> Dict:
        """load the config from a file using orjson"""
        config_data = None
        try:
            with open(filePath, "rb") as file:
                config_data = orjson.loads(file.read())
        except FileNotFoundError:
            print(f"Config file not found: {filePath}")
        except orjson.JSONDecodeError:
            print(f"Invalid JSON in config file: {filePath}")
        finally:
            assert config_data is not None, "unable to load experiment configuration"
            return config_data
        
    def _validSearchFieldLabel(self, label: str) -> bool:
        """check if the label of a search field is formatted correctly"""
        pattern = r'^([^[]+)(?:\[(\d*(?:,\d+)*)\])?'
        match = re.match(pattern, label)
        return match is not None
    
    def _extractLabelGroups(self, label: str) -> Tuple[str, str]:
        """extract the name and index from a search field label"""
        pattern = r'^([^[]+)(?:\[([^\]]*)\])?'
    
        match = re.match(pattern, label)
        assert match, f"'{label}' not a valid label; error in validity check"
        
        name = match.group(1)
        index = match.group(2) if match.group(2) else None
        return name, index
    
    def _checkIfCallectionLabel(self, label: str) -> bool:
        """check if the label of a search field is a collection label"""
        pattern = r'.*\[.*\].*'
        match = re.match(pattern, label)
        return match is not None
    
    def _parseCollection(self, field: Dict, config: UdacitySimulatorConfig) -> Tuple[List[Dict], List[Callable]]:
        label = field[fileLabels.FIELD_LABEL]

        assert self._checkIfCallectionLabel(label), f"'{label}' of a field which isn't a collection"
        fields = []
        updateMethods = []
        
        fieldName, index = self._extractLabelGroups(label)
        fieldSize = len(getattr(config, fieldName))
        indexes = []

        if(index is None):
            indexes = list(range(0, fieldSize))
        else:
            indexes = [int(x.strip()) for x in index.split(',') if x.strip()]
            
            for i in indexes:
                if i >= fieldSize:
                    raise f"index '{i}' out of bound in '{fieldName}'"
    
        for i in indexes:
            cpy = field
            fields += [cpy]
            
            def updateCollection(value, fName=fieldName, idx=i):
                collection = getattr(config, fName)
                collection[idx] = value
                setattr(config, fName, collection)
            
            updateMethods += [updateCollection]

        return fields, updateMethods 