from experimentsRunner import ExperimentConfigParser, ExperimentConfig
from experimentsRunner import ExperimentRunner
from dbInteract import MongoInteract
from dotenv import load_dotenv
from os import getenv

load_dotenv()
DB_URI = getenv('DB_URI')

parser: ExperimentConfigParser = ExperimentConfigParser()
db: MongoInteract = MongoInteract(DB_URI)
expConfig: ExperimentConfig = parser.parse("./sample.json")
expManager: ExperimentRunner = ExperimentRunner(expConfig, db)
scenarioId, expTime = expManager.run()

print(f"Experiment completed with ID: {scenarioId} in {expTime:.2f} seconds")
