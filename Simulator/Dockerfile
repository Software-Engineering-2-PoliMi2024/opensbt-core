FROM python:3.8.20-bookworm

WORKDIR /simulator

RUN apt-get update && apt-get install -y libgl1 xvfb && rm -rf /var/lib/apt/lists/*

# Add open-sbt requirements
COPY ./Simulator/lanekeeping/requirements.txt /simulator
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Add Simulation server requirements
COPY ./Simulator/requirements.txt /simulator
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Copy the simulator 
COPY ./Simulator /simulator/Simulator

# # Uvicorn will serve FastAPI on port 8000
CMD ["uvicorn", "Simulator.SimulatorServer:app", "--host", "0.0.0.0", "--port", "8000"]