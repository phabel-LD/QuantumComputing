# # Quantum Fourier Transform Counter
# 
# **Author:** Phabel Antonio López Delgado, BSc.
# 
# This notebook provides an alternative implementation of the Quantum Fourier Transform (QFT) and its inverse, focusing on a "counter" approach where qubits are indexed from least significant to most significant. It also demonstrates the use of swaps to reverse qubit order. The implementation uses `QuantumRegister` and `ClassicalRegister` for clarity.
# 
# **Key Concepts Covered:**
# - Quantum Fourier Transform with explicit registers.
# - Inverse QFT.
# - Swapping qubits to reverse order.
# - Initialisation from a binary string.
# 
# **Key Techniques & Libraries:**
# - `qiskit` – quantum circuit construction with registers.
# - `qiskit-aer` – simulation.
# - `matplotlib` – circuit visualisation.
# 
# **Objective:**
# To understand the QFT using explicit register indexing and a counter‑style implementation.


import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import CPhaseGate
from qiskit.visualization import plot_histogram
import random

# Configuration
CONFIG = {
    "n_qubits": 3,
    "shots": 1024,
    "random_seed": 42,
}

np.random.seed(CONFIG["random_seed"])
random.seed(CONFIG["random_seed"])

# Initialise simulator
qasm_sim = Aer.get_backend('qasm_simulator')

print("Configuration loaded.")
print(f"Simulator: {qasm_sim.name}")
print(f"Shots: {CONFIG['shots']}")
print(f"Number of qubits: {CONFIG['n_qubits']}")

# ## 1. Helper Functions
# 
# We define functions to create the circuit, initialise a state from a binary string, and draw circuits.


def crear_circuito(n_qubits, n_bits):
    """
    Create a quantum circuit with n_qubits qubits and n_bits classical bits.
    
    Args:
        n_qubits: Number of qubits.
        n_bits: Number of classical bits.
    
    Returns:
        tuple: (QuantumCircuit, QuantumRegister, ClassicalRegister)
    """
    q = QuantumRegister(n_qubits, name="q")
    c = ClassicalRegister(n_bits, name="c")
    qc = QuantumCircuit(q, c)
    return qc, q, c

def inicializar_estado(estado, qc, q):
    """
    Initialise the qubits from a binary string (e.g., '011').
    
    Args:
        estado: Binary string (MSB to LSB).
        qc: Quantum circuit.
        q: Quantum register.
    """
    n_qubits = len(q)
    for ind, bit in enumerate(estado):
        if bit == '1':
            qc.x(q[n_qubits - ind - 1])  # Reverse indexing to match qubit order

def draw_circuit(qc, filename='qft_counter_circuit.png'):
    """
    Draw the circuit using matplotlib and save it.
    """
    try:
        fig = qc.draw('mpl')
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()
        plt.close(fig)
    except Exception as e:
        print("Circuit drawing failed, falling back to text:")
        print(qc.draw(output='text'))

print("Helper functions defined.")

# ## 2. Quantum Fourier Transform (Counter Style)
# 
# The QFT is applied with a specific loop order that starts from the most significant qubit and works downwards. This is a common counter‑style implementation.


def QFT(qc, q, n_qubits):
    """
    Apply the Quantum Fourier Transform in counter style.
    
    Args:
        qc: Quantum circuit.
        q: Quantum register.
        n_qubits: Number of qubits.
    """
    for ind in range(n_qubits - 1, -1, -1):
        qc.h(q[ind])
        for j in range(ind - 1, -1, -1):
            qc.cp(np.pi / (2 ** (ind - j)), q[j], q[ind])

# ## 3. Inverse QFT
# 
# The inverse QFT is applied with a reversed loop order and negative phase angles.


def QFT_inversa(qc, q, n_qubits):
    """
    Apply the inverse Quantum Fourier Transform.
    
    Args:
        qc: Quantum circuit.
        q: Quantum register.
        n_qubits: Number of qubits.
    """
    for ind in range(n_qubits):
        for j in range(ind, 0, -1):
            qc.cp(-np.pi / (2 ** (1 + ind - j)), q[j - 1], q[ind])
        qc.h(q[ind])

# ## 4. Swap Function
# 
# To reverse the order of qubits, we use swap gates. This is often part of the QFT definition to align the bit order.


def cambio_estado(qc, q, n_qubits):
    """
    Swap qubits to reverse the order.
    
    Args:
        qc: Quantum circuit.
        q: Quantum register.
        n_qubits: Number of qubits.
    """
    for ind in range(n_qubits // 2):
        qc.swap(ind, n_qubits - ind - 1)

# ## 5. Full Test: QFT + Inverse QFT
# 
# We test the implementation by encoding a state (`'011'`), applying QFT, then inverse QFT, and measuring. We verify that the original state is recovered.


n_qubits = CONFIG["n_qubits"]

# Create circuit with n_qubits qubits and n_qubits classical bits
qc, q, c = crear_circuito(n_qubits, n_qubits)

# Initial state
estado_psi = '011'  # This corresponds to |3⟩ (since 011 binary = 3)
print(f"Initial state: {estado_psi}")
inicializar_estado(estado_psi, qc, q)

# Apply QFT
QFT(qc, q, n_qubits)

# Apply inverse QFT
QFT_inversa(qc, q, n_qubits)

# (Optional) Swap to reverse order if needed
# cambio_estado(qc, q, n_qubits)  # Uncomment if you want to reverse after inverse QFT

# Measure
qc.measure(q, c)

# Draw the circuit
draw_circuit(qc, 'qft_counter_circuit.png')

# Simulate
compiled = transpile(qc, qasm_sim)
job = qasm_sim.run(compiled, shots=CONFIG["shots"])
counts = job.result().get_counts()

print(f"\nMeasurement results for initial state {estado_psi}:")
print(counts)

# Plot histogram
plot_histogram(counts)
plt.savefig('qft_counter_histogram.png')
plt.show()
plt.close('all')

# ## 6. Analysis and Discussion
# 
# **Expected behaviour:**  
# The initial state `'011'` (binary 3) should be recovered after applying QFT and inverse QFT. The measurement histogram should show the bitstring `'011'` with high probability.
# 
# **Why this implementation differs:**  
# - The QFT loop starts from the most significant qubit and goes down, using controlled phase gates with angles \(\pi / 2^{k}\).
# - The inverse QFT uses negative angles and a reversed loop order.
# - The swap function is provided separately; it can be used to reverse qubit order if needed, but the QFT and inverse QFT as implemented here do not require it for correctness (the QFT definition may or may not include swaps depending on the convention).
# 
# **Key takeaway:**  
# This counter‑style implementation is another valid approach to building QFT circuits. The order of loops and the indexing of qubits can vary, but the mathematical operation remains the same.


# ## Summary
# 
# **Accomplished:**
# - Implemented QFT and inverse QFT using a counter‑style loop.
# - Used explicit `QuantumRegister` and `ClassicalRegister`.
# - Tested the circuit on a specific initial state (`'011'`).
# - Verified that QFT + inverse QFT recovers the original state.
# 
# **Key Insights:**
# - The QFT can be implemented with different loop orders.
# - The inverse QFT uses negative phases and reversed control logic.
# - Swaps are sometimes needed to reverse qubit order, depending on the convention.
# 
# **Next Steps:**
# - Explore quantum phase estimation using QFT.
# - Implement Shor's factoring algorithm.
# - Run the circuit on real quantum hardware.