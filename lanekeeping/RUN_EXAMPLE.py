from lanekeeping import UdacitySimulator, UdacitySimulatorConfig

udacityConfig = UdacitySimulatorConfig(maxTime=2)

simulator = UdacitySimulator()

result = simulator.simulate(simulator_config=udacityConfig)

simulator.killSimulation()

print(result)