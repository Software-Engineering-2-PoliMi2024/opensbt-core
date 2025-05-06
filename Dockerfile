FROM python:3.8.20-bookworm

WORKDIR /open-bst

RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

COPY ./lanekeeping/requirements.txt /open-bst
RUN pip install -r /open-bst/requirements.txt

# Copy the simulator 
COPY ./Simulator /open-bst/lanekeeping/Simulator

#Copy th drving model
COPY ./SelfDrivingModels /open-bst/lanekeeping/SelfDrivingModels

COPY ./ /open-bst

CMD ["python", "-m", "lanekeeping.udacity.run_udacity_MINE"]