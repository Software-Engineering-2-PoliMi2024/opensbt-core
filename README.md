# Useful stuff to know

By building and running the docker it will launch a shell in the container with all the dependencies installed.
The current directory is mounted in the container at `./se2rpCODEBASE`, so you can edit files and run them directly.

To get a reference on how to run a simulation, you can run the `runExperiment.py` script.

## Docker

To build and/or run the Docker container, you can use the `DockerManager.sh` script.

## .env file for mongo DB connection

insert the `.env` file into the  `./open-bst` folder

to import and use the credentials in python code use:

```py
from dotenv import load_dotenv
from os import getenv

load_dotenv()
DB_URI = getenv('DB_URI')
```

## json input for experiment configurations

the experiment configuration have two main objects in the hash:

first the `scenario` which defines the basic configuration.
By default the scenario configuration is setted with the following values:

```py
map_size: int = 250
initial_position: tuple = (125.0, 0.0, -28.0, 8.0)
maxSpeed: float = 30.0  # Maximum speed of the ego vehicle in the simulation
minSpeed: float = 0.0  # Minimum speed of the ego vehicle in the simulation
maxTime: int = 30  # Maximum time in seconds for the simulation to run
# Maximum cross-track error (XTE) allowed, if negative, no limit is applied
maxXTE: float = 3.0
segLength: float = 25.0  # Length of each segment in the road
# Angles for the road segments, to be set during simulation
angles: List[int] = (0, 0, 0, 0, 0)
```

the second part is the definition of an array of search parameters.
Each search parameter is defined by three characteristics:

- `label`: the name of the parameter to be modified in the simulation. Must match a key in the scenario object.
- `step`: the step size for the parameter, which defines how much the parameter will change in each iteration.
- `range`: a list of two values, the first is the minimum value and the second is the maximum value.

an example of a json input file for an experiment configuration is the following:

```json
{
    "scenario" : {
        "maxSpeed": 30.0,
        "minSpeed": 0.0,
        "maxTime": 30,
        "maxXTE": 10.0,
        "segLength": 25.0,
        "angles": [0, 35, 0, -60, 0]
    },
    "searchParams" : [
        {
            "label" : "minSpeed",
            "step" : 1,
            "range" : [-20, -1]
        }
    ]
}
```

for the parameters which are defined by a collection of values, like the angles is it possible to define:

- specify the value to modify in the collection

    ```json
    "searchParams" : [
            {
                "label" : "angles[0]",
                "step" : 1,
                "range" : [-20, -1]
            }
        ]
    ```

- select multiple values in the collection. The specified `step` and `range` will be applied to all the values in the collection.

    ```json
    "searchParams" : [
            {
                "label" : "angles[0, 1, 2]",
                "step" : 1,
                "range" : [-20, -1]
            }
        ]
    ```

- modify all the values in the collection. The specified `step` and `range` will be applied to all the values in the collection.

    ```json
    "searchParams" : [
            {
                "label" : "angles[]",
                "step" : 1,
                "range" : [-20, -1]
            }
        ]
    ```
