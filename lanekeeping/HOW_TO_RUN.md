# How to run a simulation
In this package you can find a UdacitySimulatorConfig class containing all the configs of the simulation.

To run a simulation you can do:

```python 
from lanekeeping import UdacitySimulator, UdacitySimulatorConfig

udacityConfig = UdacitySimulatorConfig()

result = UdacitySimulator.simulate(simulator_config=udacityConfig)
```