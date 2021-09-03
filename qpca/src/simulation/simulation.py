import cirq


def simulate(circuit, repetitions, measurement_key):
    simulator = cirq.Simulator()
    samples = simulator.run(circuit, repetitions=repetitions)
    histogram = samples.histogram(key=measurement_key)
    return {'samples': samples, 'histogram': histogram}
