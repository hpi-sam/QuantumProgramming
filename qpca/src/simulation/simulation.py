import cirq


def simulate(circuit, repetitions, measurement_key):
    simulator = cirq.Simulator()
    samples = simulator.run(circuit, repetitions=repetitions)
    result = samples.histogram(key=measurement_key)
    return result
