# # Quantum Teleportation
# 
# **Author:** Phabel Antonio López Delgado, BSc.
# 
# Quantum teleportation is a protocol that allows the transfer of an unknown quantum state from one party (Alice) to another (Bob) using a shared entangled pair and classical communication. It is a fundamental building block of quantum communication and quantum networks.
# 
# In this notebook, we implement the full teleportation protocol step by step, including state preparation, entanglement, basis change, measurement, and conditional operations on Bob's qubit. We verify the protocol by comparing the teleported state's probabilities with the original state.
# 
# **Key Concepts Covered:**
# - Quantum teleportation protocol.
# - Bell state generation.
# - Basis change (CNOT + Hadamard).
# - Conditional operations (X and Z gates).
# - Verification of successful teleportation.
# 
# **Key Techniques & Libraries:**
# - `qiskit` – quantum circuit construction with registers.
# - `qiskit-aer` – simulation.
# - `matplotlib` – circuit visualisation.
# 
# **Objective:**
# To implement and verify the quantum teleportation protocol for arbitrary input states.


import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import random

# Configuration
CONFIG = {
    "shots": 1024,
    "random_seed": 42,
}

np.random.seed(CONFIG["random_seed"])
random.seed(CONFIG["random_seed"])

# Initialise simulator
simulator = AerSimulator()

print("Configuration loaded.")
print(f"Simulator: {simulator.name}")
print(f"Shots: {CONFIG['shots']}")

# ## 1. Helper Functions
# 
# We define functions to create the circuit, initialise a state, entangle qubits, change basis, and perform measurement with conditional decoding.


def crear_circuito():
    """
    Create a quantum circuit with three qubits (S, A, B) and three classical bits.
    
    Returns:
        tuple: (qc, q_S, q_A, q_B, c_S, c_A, c_B)
    """
    q_S = QuantumRegister(1, name='S')
    q_A = QuantumRegister(1, name='A')
    q_B = QuantumRegister(1, name='B')
    c_S = ClassicalRegister(1, name='cS')
    c_A = ClassicalRegister(1, name='cA')
    c_B = ClassicalRegister(1, name='cB')
    qc = QuantumCircuit(q_S, q_A, q_B, c_S, c_A, c_B)
    return qc, q_S, q_A, q_B, c_S, c_A, c_B

def inicializar_estado(estado, qc, q_S):
    """
    Initialise qubit S with a given state vector.
    
    Args:
        estado: List of two complex numbers [alpha, beta].
        qc: Quantum circuit.
        q_S: Quantum register for qubit S.
    """
    qc.initialize(estado, q_S[0])

def entrelazar_par(qc, q_A, q_B):
    """
    Create a Bell state between qubits A and B.
    
    Args:
        qc: Quantum circuit.
        q_A: Quantum register for qubit A.
        q_B: Quantum register for qubit B.
    """
    qc.h(q_A[0])
    qc.cx(q_A[0], q_B[0])

def cambiar_base(qc, q_S, q_A):
    """
    Apply CNOT and Hadamard to change basis (Alice's part).
    
    Args:
        qc: Quantum circuit.
        q_S: Quantum register for qubit S.
        q_A: Quantum register for qubit A.
    """
    qc.cx(q_S[0], q_A[0])
    qc.h(q_S[0])

def medicion_decodificar(qc, q_S, q_A, q_B, c_S, c_A, c_B):
    """
    Measure qubits S and A, then apply conditional X and Z gates to qubit B.
    
    Args:
        qc: Quantum circuit.
        q_S, q_A, q_B: Quantum registers.
        c_S, c_A, c_B: Classical registers.
    """
    qc.measure(q_S[0], c_S[0])
    qc.measure(q_A[0], c_A[0])
    # Conditional operations on Bob's qubit
    with qc.if_test((c_A[0], 1)):
        qc.x(q_B[0])
    with qc.if_test((c_S[0], 1)):
        qc.z(q_B[0])
    qc.measure(q_B[0], c_B[0])

def draw_circuit(qc, filename='teleport_circuit.png'):
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

# ## 2. Full Teleportation Circuit
# 
# We combine the steps into a single function that builds the complete circuit for a given input state.


def circuito_teleportacion(estado):
    """
    Build the full quantum teleportation circuit for a given input state.
    
    Args:
        estado: List of two complex numbers [alpha, beta].
    
    Returns:
        QuantumCircuit: Complete teleportation circuit.
    """
    qc, q_S, q_A, q_B, c_S, c_A, c_B = crear_circuito()
    inicializar_estado(estado, qc, q_S)
    entrelazar_par(qc, q_A, q_B)
    cambiar_base(qc, q_S, q_A)
    medicion_decodificar(qc, q_S, q_A, q_B, c_S, c_A, c_B)
    return qc

# ## 3. Verification Functions
# 
# We define functions to normalise a state, compare probabilities, and run the teleportation circuit for verification.


def normalizar_estado(estado):
    """
    Normalise a quantum state vector.
    
    Args:
        estado: List of two complex numbers [alpha, beta].
    
    Returns:
        np.ndarray: Normalised state vector.
    """
    estado = np.array(estado)
    norm = np.linalg.norm(estado)
    if norm == 0:
        raise ValueError("The state cannot be the zero vector.")
    return estado / norm

def calcular_similitud(estado_entrada, counts):
    """
    Compare the expected probabilities of the input state with the observed probabilities of Bob's qubit.
    
    Args:
        estado_entrada: List of two complex numbers [alpha, beta].
        counts: Dictionary of measurement counts.
    
    Returns:
        tuple: (errors, observed_probabilities)
    """
    prob_esperadas = [abs(x)**2 for x in estado_entrada]
    total = sum(counts.values())
    count_0 = sum(count for outcome, count in counts.items() if outcome[0] == '0')
    count_1 = sum(count for outcome, count in counts.items() if outcome[0] == '1')
    prob_observadas = [count_0 / total, count_1 / total]
    errors = [abs(x - y) for x, y in zip(prob_esperadas, prob_observadas)]
    return errors, prob_observadas

def verificacion_probabilidad(estado_entrada, shots=1024):
    """
    Run the teleportation circuit and verify that Bob's qubit matches the input state probabilities.
    
    Args:
        estado_entrada: List of two complex numbers [alpha, beta].
        shots: Number of simulation shots.
    
    Returns:
        list: Observed probabilities for Bob's qubit.
    """
    estado_original = normalizar_estado(estado_entrada)
    print(f"Original state: |psi> = ({estado_original[0]:.4f})|0> + ({estado_original[1]:.4f})|1>")
    
    # Build and simulate the circuit
    qc = circuito_teleportacion(estado_original)
    compiled = transpile(qc, simulator)
    job = simulator.run(compiled, shots=shots)
    counts = job.result().get_counts()
    
    # Calculate errors and observed probabilities
    errors, prob_salida = calcular_similitud(estado_original, counts)
    
    # Print results
    prob_esperadas = [abs(x)**2 for x in estado_original]
    print(f"Expected probabilities: P(0) = {prob_esperadas[0]:.4f}, P(1) = {prob_esperadas[1]:.4f}")
    print(f"Observed probabilities: P(0) = {prob_salida[0]:.4f}, P(1) = {prob_salida[1]:.4f}")
    print(f"Differences: Delta P(0) = {errors[0]:.4f}, Delta P(1) = {errors[1]:.4f}")
    
    if max(errors) < 0.05:
        print("Result: Probabilities match. Teleportation successful.")
    else:
        print("Result: Probabilities do not match. Teleportation may have errors.")
    
    return prob_salida

print("Verification functions defined (corrected).")

# ## 4. Test on Various Input States
# 
# We test the teleportation protocol on a selection of input states, including basis states and superposition states.


# Test states
test_states = [
    ([1, 0], "State |0>"),
    ([0, 1], "State |1>"),
    ([1/np.sqrt(2), 1/np.sqrt(2)], "State |+>"),
    ([1/np.sqrt(2), -1/np.sqrt(2)], "State |->"),
    ([np.sqrt(3)/2, 1/2], "State sqrt(3)/2|0> + 1/2|1>"),
    ([0.8, 0.6], "State 0.8|0> + 0.6|1>"),
]

print("Quantum Teleportation Verification")
print("=" * 60)

for state, description in test_states:
    print(f"\nTest: {description}")
    print("-" * 60)
    verificacion_probabilidad(state, shots=CONFIG["shots"])

# ## 5. Circuit Visualisation for a Specific State
# 
# We draw the full teleportation circuit for one example state.


# Example state
example_state = [1/np.sqrt(2), 1j/np.sqrt(2)]
qc = circuito_teleportacion(example_state)
draw_circuit(qc, 'teleport_circuit_example.png')
print(f"Circuit for state: (1/√2)|0> + (i/√2)|1>")

# ## 6. Analysis and Discussion
# 
# **Expected behaviour:**  
# The teleportation protocol should transfer the input state from Alice's qubit S to Bob's qubit B with high fidelity. The verification compares the probabilities of measuring Bob's qubit in |0> and |1> with the expected probabilities from the input state. For a perfect teleportation, the probabilities should match.
# 
# **Why does it work?**  
# 1. Alice and Bob share an entangled Bell pair.
# 2. Alice performs a Bell measurement on her qubits (S and A).
# 3. The measurement outcome tells Bob which operations (X and/or Z) to apply to his qubit to recover the original state.
# 4. After applying the corrections, Bob's qubit is in the same state as Alice's original qubit.
# 
# **Key insight:**  
# The protocol uses entanglement as a resource and classical communication to transfer quantum information. It does not allow faster-than-light communication because the classical information travel is limited by the speed of light, but it demonstrates the fundamental principles of quantum communication.


# ## Summary
# 
# **Accomplished:**
# - Implemented the full quantum teleportation protocol.
# - Tested the protocol on multiple input states (basis and superposition).
# - Verified that the probabilities of Bob's qubit match those of the input state.
# - Visualised the teleportation circuit.
# 
# **Key Insights:**
# - Teleportation relies on entanglement and classical communication.
# - Conditional operations (X and Z) correct Bob's qubit based on Alice's measurement.
# - The protocol works for arbitrary states, including complex superpositions.
# 
# **Next Steps:**
# - Run the protocol on real quantum hardware.
# - Extend to multi‑qubit teleportation.
# - Explore quantum repeaters and quantum networks.