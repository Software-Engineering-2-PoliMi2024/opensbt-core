FROM python:3.8.20-bookworm

WORKDIR /open-bst

RUN apt-get update && apt-get install -y libgl1 xvfb && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /open-bst
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Copy the simulator 
COPY ./Simulator /open-bst/lanekeeping/Simulator

# #Copy the driving model
COPY ./SelfDrivingModels /open-bst/lanekeeping/SelfDrivingModels

# COPY ./ /open-bst

# CMD ["python", "-m", "lanekeeping.udacity.run_udacity_MINE"]