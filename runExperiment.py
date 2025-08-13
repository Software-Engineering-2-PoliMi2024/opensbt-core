from experimentsRunner import ExperimentConfigParser, ExperimentConfig
from experimentsRunner import ExperimentRunner
from dbInteract import MongoInteract

DB_URI = 'mongodb+srv://matteo5figini:u1pJGtNXTqn5gTiP@se2db.tdibt7g.mongodb.net/?retryWrites=true&w=majority&appName=se2db'

parser: ExperimentConfigParser = ExperimentConfigParser()
db: MongoInteract = MongoInteract(DB_URI)
expConfig: ExperimentConfig = parser.parse("./sample.json")
expManager: ExperimentRunner = ExperimentRunner(expConfig, db)
scenarioId, expTime = expManager.run()

print(f"Experiment completed with ID: {scenarioId} in {expTime:.2f} seconds")
