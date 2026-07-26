# # Even/Odd Parity Checking Circuit
# 
# **Author:** Phabel Antonio López Delgado, BSc.
# 
# This notebook implements a simple quantum circuit that demonstrates superposition and measurement by creating a state that can be interpreted as even/odd parity. We place two qubits in superposition, apply an X gate to one qubit, and measure both. The measurement results show the two possible outcomes (00 and 11) or (01 and 10) depending on the circuit.
# 
# **Key Concepts Covered:**
# - Superposition with Hadamard gates.
# - X gate (NOT) on a single qubit.
# - Measurement and histogram visualisation.
# - Statevector visualisation.
# 
# **Key Techniques & Libraries:**
# - `qiskit` – quantum circuit construction.
# - `qiskit-aer` – simulation backends.
# - `matplotlib` – circuit drawing and histogram plotting.
# 
# **Objective:**
# To understand how superposition and measurement work in a simple two‑qubit circuit.


import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector, circuit_drawer
import random

# Configuration
CONFIG = {
    "shots": 1024,
    "random_seed": 42,
}

np.random.seed(CONFIG["random_seed"])
random.seed(CONFIG["random_seed"])

# Initialise simulator backends
statevector_sim = Aer.get_backend('statevector_simulator')
qasm_sim = Aer.get_backend('qasm_simulator')

print("Configuration loaded.")
print(f"Statevector simulator: {statevector_sim.name}")
print(f"QASM simulator: {qasm_sim.name}")
print(f"Shots: {CONFIG['shots']}")

# ## 1. Circuit Construction
# 
# We create a circuit with two qubits and two classical bits. The steps:
# 1. Apply Hadamard gates to both qubits (creates superposition).
# 2. Apply an X gate to qubit 1 (flips it).
# 3. Add a barrier for visual clarity.
# 4. Measure qubit 0 into classical bit 0, and qubit 1 into classical bit 1.
# 
# The expected measurement outcomes will be either `00` and `11` (if the X gate is on qubit 0) or `01` and `10` (if on qubit 1). Here we place X on qubit 1, so the outcomes should be `01` and `10` with equal probability.


# Create circuit
qcirc = QuantumCircuit(2, 2)

# Superposition
qcirc.h(0)
qcirc.h(1)

# X gate on qubit 1
qcirc.x(1)

# Barrier
qcirc.barrier()

# Measure
qcirc.measure(0, 0)
qcirc.measure(1, 1)

# Draw circuit using matplotlib
try:
    fig = qcirc.draw('mpl')
    fig.savefig('evenodd_circuit.png', dpi=150, bbox_inches='tight')
    plt.show()
    plt.close(fig)
except Exception as e:
    print("Matplotlib drawing failed, falling back to text:")
    print(qcirc.draw(output='text'))

# ## 2. Statevector Visualisation
# 
# We first obtain the statevector of the circuit without measurement to see the superposition state.


# Circuit for statevector (without measurement)
qc_state = QuantumCircuit(2)
qc_state.h(0)
qc_state.h(1)
qc_state.x(1)

# Simulate
compiled_state = transpile(qc_state, statevector_sim)
job_state = statevector_sim.run(compiled_state)
statevector = job_state.result().get_statevector()

print(f"Statevector:\n{statevector}")
print(f"\nProbabilities:\n{np.abs(statevector)**2}")

# ## 3. Measurement and Histogram
# 
# We run the circuit on the QASM simulator with 1024 shots and plot the histogram of measurement results.


# Compile and run on QASM simulator
compiled_qasm = transpile(qcirc, qasm_sim)
job_qasm = qasm_sim.run(compiled_qasm, shots=CONFIG["shots"])
counts = job_qasm.result().get_counts()

print(f"Measurement results:")
print(counts)

# Plot histogram
plot_histogram(counts)
plt.savefig('evenodd_histogram.png')
plt.show()
plt.close('all')

# ## 4. Analysis
# 
# The circuit applies Hadamard gates to both qubits, creating the superposition state:
# 
# $$
# |\psi_0\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle)
# $$
# 
# Then the X gate on qubit 1 flips the second qubit:
# 
# $$
# X_1 |\psi_0\rangle = \frac{1}{2}(|01\rangle + |00\rangle + |11\rangle + |10\rangle)
# $$
# 
# Since the amplitudes are all equal (each basis state has probability $1/4$), the X gate simply reorders the basis states but does not change the probability distribution.
# 
# After measurement, the histogram will show roughly equal counts for all four basis states ($|00\rangle$, $|01\rangle$, $|10\rangle$, $|11\rangle$) with approximately 25% each, within statistical fluctuations due to the finite number of shots (1024).
# 
# **Key mathematical insight:** The state remains a uniform superposition, demonstrating that superposition and measurement produce a random outcome with uniform probability when all basis states are equally likely.


# ## Summary
# 
# **Accomplished:**
# - Built a two‑qubit circuit with Hadamard gates, an X gate, and measurement.
# - Visualised the circuit diagram and statevector.
# - Ran the circuit on a simulator and obtained measurement histograms.
# 
# **Key Insights:**
# - Superposition creates all possible states with equal amplitude.
# - The X gate flips the state of a qubit.
# - Measurement collapses the superposition to a single basis state.
# - The histogram reflects the probability distribution.
# 
# **Next Steps:**
# - Explore the Deutsch‑Jozsa algorithm to see how superposition can solve problems faster.
# - Investigate entanglement and its role in quantum algorithms.