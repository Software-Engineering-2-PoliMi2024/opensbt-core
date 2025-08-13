from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from dataclasses import asdict
from fastapi.encoders import jsonable_encoder
import numpy as np
from queue import Queue
import uuid
from threading import Thread
from lanekeeping import UdacitySimulatorConfig, UdacitySimulator, SimulationOutput


app = FastAPI()

# Job tracking
jobQueue = Queue()
results = {}

def simulationThread():
    simulator = UdacitySimulator()

    while True:
        #Fetches a job from the queue
        jobId, config = jobQueue.get(block=True)

        try:
            #Performs the simulation
            simOutput : SimulationOutput = simulator.simulate(simulator_config=config)

            #Parse the output into a json
            output = jsonable_encoder(simOutput, custom_encoder={
                    np.float32: float,
                    np.float64: float
                })
            
            #Add output to results
            results[jobId] = {"status": "done", "output": output}
        except Exception as e:
            #Add error to the results
            results[jobId] = {"status": "error", "error": str(e)}
        finally:
            jobQueue.task_done()

# Start simulator thread
Thread(target=simulationThread).start()

@app.post("/simulate")
async def simulate(config: UdacitySimulatorConfig):
    #Generate a unique jobId
    jobId = str(uuid.uuid4())

    #Set the status as queued
    results[jobId] = {"status" : "queued"}

    #Enqueues the job
    jobQueue.put((jobId, config))

    #Returns the job id
    return {'jobId': jobId}


@app.get("/simulate/{job_id}")
def get_result(job_id: str):
    return results.get(job_id, {"status": "not_found"})