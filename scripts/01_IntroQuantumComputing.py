# # Introduction to Quantum Computing
# 
# **Author:** Phabel Antonio López Delgado, BSc.
# 
# This notebook introduces the fundamental concepts of quantum computing using Qiskit. We explore qubits, quantum gates, superposition, entanglement, and measurement. We also introduce the quantum circuit model and visualise quantum states.
# 
# **Key Concepts Covered:**
# - Qubits and quantum states.
# - Single‑qubit gates (X, H, Z, etc.).
# - Multi‑qubit gates (CNOT, SWAP, etc.).
# - Superposition and entanglement.
# - Measurement and state visualisation.
# 
# **Key Techniques & Libraries:**
# - `qiskit` – quantum circuit construction and simulation.
# - `qiskit-aer` – AerSimulator for statevector and shot‑based simulation.
# - `matplotlib` – circuit visualisation and histogram plotting.
# 
# **Objective:**
# To build a foundational understanding of quantum circuits and their simulation using Qiskit.


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

# Set seeds for reproducibility
np.random.seed(CONFIG["random_seed"])
random.seed(CONFIG["random_seed"])

# Initialise simulator backends
statevector_sim = Aer.get_backend('statevector_simulator')
qasm_sim = Aer.get_backend('qasm_simulator')

print("Configuration loaded.")
print(f"Statevector simulator: {statevector_sim.name}")
print(f"QASM simulator: {qasm_sim.name}")
print(f"Shots: {CONFIG['shots']}")

# ## 1. Single Qubit Gates
# 
# We create a quantum circuit with one qubit and apply basic gates: X (NOT), H (Hadamard), Z, and others. We visualise the circuit and the state vector on the Bloch sphere.


# Create a circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)

# Apply X gate (NOT)
qc.x(0)

# Measure
qc.measure(0, 0)

# Draw the circuit
print("Circuit with X gate:")
print(qc.draw(output='text'))

# Simulate on QASM simulator
compiled = transpile(qc, qasm_sim)
job = qasm_sim.run(compiled, shots=CONFIG["shots"])
result = job.result()
counts = result.get_counts()

print("\nMeasurement results:")
print(counts)

# Visualise histogram
plot_histogram(counts)
plt.savefig('x_gate_histogram.png')
plt.show()
plt.close('all')

# Hadamard gate (creates superposition)
qc_h = QuantumCircuit(1, 1)
qc_h.h(0)
qc_h.measure(0, 0)

print("Circuit with H gate:")
print(qc_h.draw(output='text'))

compiled_h = transpile(qc_h, qasm_sim)
job_h = qasm_sim.run(compiled_h, shots=CONFIG["shots"])
counts_h = job_h.result().get_counts()

print("\nMeasurement results (superposition):")
print(counts_h)
print(f"Probability of |0⟩: {counts_h.get('0', 0) / CONFIG['shots']:.2f}")
print(f"Probability of |1⟩: {counts_h.get('1', 0) / CONFIG['shots']:.2f}")

plot_histogram(counts_h)
plt.savefig('h_gate_histogram.png')
plt.show()
plt.close('all')

# Visualise state vector on Bloch sphere (without measurement)
qc_state = QuantumCircuit(1)
qc_state.h(0)

compiled_state = transpile(qc_state, statevector_sim)
job_state = statevector_sim.run(compiled_state)
statevector = job_state.result().get_statevector()

print(f"State vector: {statevector}")
plot_bloch_multivector(statevector)
plt.savefig('bloch_sphere.png')
plt.show()
plt.close('all')

# ## 2. Example: Superposition with X Gate and Measurement (Swapped Bits)
# 
# We build a circuit with two qubits. Both are placed in superposition using Hadamard gates, then we apply an X gate on qubit 1. We add a barrier for visual clarity, then measure qubit 0 into classical bit 1 and qubit 1 into classical bit 0 (swapped). We then display the statevector and the measurement histogram.


# Create circuit with 2 qubits and 2 classical bits
qcirc = QuantumCircuit(2, 2)

# Superposition with two Hadamard gates
qcirc.h(0)
qcirc.h(1)

# X gate on qubit 1
qcirc.x(1)

# Barrier for visualisation
qcirc.barrier()

# Measure with swapped mapping: qubit 0 -> classical bit 1, qubit 1 -> classical bit 0
qcirc.measure(0, 1)
qcirc.measure(1, 0)

# Draw the circuit (using 'mpl' for a nicer image, but fallback to 'text' if needed)
try:
    qcirc.draw('mpl')
    plt.savefig('circuit_with_x.png')
    plt.show()
except:
    print(qcirc.draw(output='text'))

# Get statevector before measurement (without classical bits)
qc_state = QuantumCircuit(2)
qc_state.h(0)
qc_state.h(1)
qc_state.x(1)
# Note: we don't include measurement for statevector
compiled_state = transpile(qc_state, statevector_sim)
job_state = statevector_sim.run(compiled_state)
outputstate = job_state.result().get_statevector()
print(f"\nStatevector (before measurement):\n{outputstate}")

# Now simulate with measurement on QASM
compiled_qasm = transpile(qcirc, qasm_sim)
job_qasm = qasm_sim.run(compiled_qasm, shots=CONFIG["shots"])
counts = job_qasm.result().get_counts()

print(f"\nMeasurement results (swapped bits):")
print(counts)

# Plot histogram
plot_histogram(counts)
plt.savefig('histogram_with_x.png')
plt.show()
plt.close('all')

# ## 3. Multi‑Qubit Gates and Entanglement (Bell State)
# 
# We create a Bell state (|00⟩ + |11⟩)/√2 using a Hadamard gate followed by a CNOT gate. This demonstrates entanglement.


# Create Bell state circuit
qc_bell = QuantumCircuit(2, 2)
qc_bell.h(0)
qc_bell.cx(0, 1)
qc_bell.measure([0, 1], [0, 1])

print("Bell state circuit:")
print(qc_bell.draw(output='text'))

compiled_bell = transpile(qc_bell, qasm_sim)
job_bell = qasm_sim.run(compiled_bell, shots=CONFIG["shots"])
counts_bell = job_bell.result().get_counts()

print("\nMeasurement results (Bell state):")
print(counts_bell)

plot_histogram(counts_bell)
plt.savefig('bell_state_histogram.png')
plt.show()
plt.close('all')

# Visualise Bell state vector
qc_bell_state = QuantumCircuit(2)
qc_bell_state.h(0)
qc_bell_state.cx(0, 1)

compiled_bell_state = transpile(qc_bell_state, statevector_sim)
job_bell_state = statevector_sim.run(compiled_bell_state)
bell_statevector = job_bell_state.result().get_statevector()

print(f"Bell state vector:\n{bell_statevector}")
print(f"Probabilities: {np.abs(bell_statevector)**2}")

# ## 4. Quantum Teleportation (Preview)
# 
# We implement a simple teleportation circuit to demonstrate quantum communication.


# Quantum teleportation circuit
qc_teleport = QuantumCircuit(3, 1)

# Create Bell pair (qubits 1 and 2)
qc_teleport.h(1)
qc_teleport.cx(1, 2)

# Prepare state to send on qubit 0 (|+⟩ state)
qc_teleport.h(0)

# Teleportation sequence
qc_teleport.cx(0, 1)
qc_teleport.h(0)
qc_teleport.measure(0, 0)
qc_teleport.measure(1, 0)

print("Teleportation circuit:")
print(qc_teleport.draw(output='text'))

compiled_teleport = transpile(qc_teleport, qasm_sim)
job_teleport = qasm_sim.run(compiled_teleport, shots=CONFIG["shots"])
counts_teleport = job_teleport.result().get_counts()

print("\nMeasurement results:")
print(counts_teleport)

plot_histogram(counts_teleport)
plt.savefig('teleport_histogram.png')
plt.show()
plt.close('all')

# ## Summary
# 
# **Accomplished:**
# - Created and simulated quantum circuits with Qiskit.
# - Applied single‑qubit gates (X, H) and observed superposition.
# - Built a two‑qubit circuit with Hadamards, X gate, and swapped measurement.
# - Generated entanglement using the Bell state.
# - Previewed quantum teleportation.
# 
# **Key Insights:**
# - The Hadamard gate creates superposition, giving equal probability for |0⟩ and |1⟩.
# - CNOT gates entangle qubits, producing correlated measurement outcomes.
# - Swapping classical bit mappings is possible and demonstrates flexibility in circuit design.
# - Quantum states can be visualised on the Bloch sphere, as statevectors, and as histograms.
# 
# **Next Steps:**
# - Explore Deutsch‑Jozsa algorithm for function classification.
# - Implement Grover's search algorithm.
# - Study Quantum Fourier Transform and phase estimation.
# - Run circuits on real quantum hardware via IBM Quantum.