from experimentsRunner import ExperimentConfigParser
from experimentsRunner import ExperimentRunner
from dbInteract import MongoInteract

DB_URI = 'mongodb+srv://matteo5figini:u1pJGtNXTqn5gTiP@se2db.tdibt7g.mongodb.net/?retryWrites=true&w=majority&appName=se2db'

parser = ExperimentConfigParser()
db = MongoInteract(DB_URI)
expConfig = parser.parse("./sample.json")
expManager = ExperimentRunner(expConfig, db)
scenarioId, expTime = expManager.run()

print(f"Experiment completed with ID: {scenarioId} in {expTime:.2f} seconds")