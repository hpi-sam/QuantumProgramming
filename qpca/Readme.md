# Overview
In this project a quantum based PCA algorithm is implemented.
The quantum modules are integrated into a classical computing environment as follows:

* Classical preprocessing to compute necessary unitary operations
* Quantum modules:
  * Swap test
  * Quantum Phase Estimation
* Classical preprocessing to compute the eigenvalues


## Open Tasks
During the project phase the program logic, how to transform classical data into quantum state could not be implemented.
Therefore, no "main" file to run the PCA algorithm exists yet.

The following tasks are open:
* Unitary operation for quantum state initialization
* Universal logic to compute qpe unitary operation (depends on initialized quantum state)


## Test Runner
The used example data sets can be found in src > tests > test_data_sets.py

To run all test cases the test runner can be called as follows:
```
python ./src/tests/test_runner.py
```
