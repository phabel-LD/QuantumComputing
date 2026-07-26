# # Deutsch‑Jozsa Algorithm
# 
# **Author:** Phabel Antonio López Delgado, BSc.
# 
# The Deutsch‑Jozsa algorithm is one of the first examples of a quantum algorithm that achieves exponential speedup over classical algorithms. It determines whether a given function \( f: \{0,1\}^n \rightarrow \{0,1\} \) is **constant** (returns the same value for all inputs) or **balanced** (returns 0 for exactly half of the inputs and 1 for the other half) using a single query to the quantum oracle.
# 
# **Key Concepts Covered:**
# - Quantum oracles for constant and balanced functions.
# - Superposition and phase kickback.
# - Quantum parallelism.
# - Measurement and interpretation of results.
# 
# **Key Techniques & Libraries:**
# - `qiskit` – quantum circuit construction.
# - `qiskit-aer` – simulation backends.
# - `matplotlib` – circuit drawing and histogram plotting.
# 
# **Objective:**
# To implement the Deutsch‑Jozsa algorithm for an arbitrary number of qubits and verify its behaviour for constant and balanced oracles.


import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
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
qasm_sim = Aer.get_backend('qasm_simulator')

print("Configuration loaded.")
print(f"Simulator: {qasm_sim.name}")
print(f"Shots: {CONFIG['shots']}")

# ## 1. Oracle Functions
# 
# We define two types of oracles:
# 
# - **Constant oracle** – returns the same value (0 or 1) for all inputs.
# - **Balanced oracle** – returns 0 for half the inputs and 1 for the other half.
# 
# The oracle is implemented as a quantum circuit that acts on \( n \) input qubits and one auxiliary qubit.


def oracle_constant(n, value=0):
    """
    Create a constant oracle.
    
    Args:
        n: Number of input qubits.
        value: Constant value to return (0 or 1).
    
    Returns:
        QuantumCircuit: Oracle circuit.
    """
    oracle = QuantumCircuit(n + 1)  # n input + 1 auxiliary
    
    if value == 1:
        # If constant 1, flip the auxiliary qubit
        oracle.x(n)
    
    return oracle

def oracle_balanced(n):
    """
    Create a balanced oracle using CNOT gates from each input qubit to the auxiliary.
    
    Args:
        n: Number of input qubits.
    
    Returns:
        QuantumCircuit: Oracle circuit.
    """
    oracle = QuantumCircuit(n + 1)
    for qubit in range(n):
        oracle.cx(qubit, n)
    return oracle

print("Oracle functions defined.")

# ## 2. Deutsch‑Jozsa Circuit
# 
# The algorithm applies:
# 
# 1. Hadamard gates to all input qubits to create superposition.
# 2. X gate on the auxiliary qubit to prepare it in state |1⟩.
# 3. Hadamard gate on the auxiliary qubit.
# 4. The oracle.
# 5. Hadamard gates on all input qubits.
# 6. Measurement of the input qubits.
# 
# If all measured qubits are |0⟩, the function is constant; otherwise, it is balanced.


def deutsch_joza_circuit(n, oracle):
    """
    Build the Deutsch‑Jozsa circuit for n qubits with the given oracle.
    
    Args:
        n: Number of input qubits.
        oracle: QuantumCircuit oracle.
    
    Returns:
        QuantumCircuit: Complete Deutsch‑Jozsa circuit.
    """
    # Circuit with n input qubits + 1 auxiliary, and n classical bits
    qc = QuantumCircuit(n + 1, n)
    
    # Step 1: Superposition on input qubits
    for qubit in range(n):
        qc.h(qubit)
    
    # Step 2: Prepare auxiliary qubit in |1⟩ and apply Hadamard
    qc.x(n)
    qc.h(n)
    
    # Step 3: Apply the oracle
    qc.compose(oracle, inplace=True)
    
    # Step 4: Hadamard on input qubits
    for qubit in range(n):
        qc.h(qubit)
    
    # Step 5: Measure input qubits
    qc.measure(range(n), range(n))
    
    return qc

# ## 3. Run the Algorithm
# 
# We run the Deutsch‑Jozsa algorithm for \( n = 2 \) qubits using both a constant oracle (returning 0) and a balanced oracle. We visualise the circuit and the measurement histogram.


def run_deutsch_joza(n, oracle, oracle_type="constant"):
    """
    Run the Deutsch‑Jozsa algorithm and interpret the results.
    """
    # Build the circuit
    qc = deutsch_joza_circuit(n, oracle)
    
    # Draw the circuit
    try:
        fig = qc.draw('mpl')
        fig.savefig(f'dj_circuit_{oracle_type}_{n}.png', dpi=150, bbox_inches='tight')
        plt.show()
        plt.close(fig)
    except Exception as e:
        print("Circuit drawing failed, falling back to text:")
        print(qc.draw(output='text'))
    
    # Simulate
    compiled = transpile(qc, qasm_sim)
    job = qasm_sim.run(compiled, shots=CONFIG["shots"])
    counts = job.result().get_counts()
    
    # Plot histogram
    plot_histogram(counts)
    plt.savefig(f'dj_histogram_{oracle_type}_{n}.png')
    plt.show()
    plt.close('all')
    
    # Interpret results
    print(f"\nResults for {oracle_type} oracle (n={n}):")
    print(counts)
    
    if '0' * n in counts and len(counts) == 1:
        print("Interpretation: The function is CONSTANT.")
    else:
        print("Interpretation: The function is BALANCED.")
    
    # Show frequencies
    for state, freq in counts.items():
        print(f"State: {state} -> {freq} ({freq / CONFIG['shots']:.2%})")
    
    return counts

# ### 3.1 Constant Oracle (returns 0)


n_qubits = 2
oracle_const = oracle_constant(n_qubits, value=0)
counts_const = run_deutsch_joza(n_qubits, oracle_const, oracle_type="constant_0")

oracle_const_1 = oracle_constant(n_qubits, value=1)
counts_const_1 = run_deutsch_joza(n_qubits, oracle_const_1, oracle_type="constant_1")

# ### 3.3 Balanced Oracle


oracle_bal = oracle_balanced(n_qubits)
counts_bal = run_deutsch_joza(n_qubits, oracle_bal, oracle_type="balanced")

# ## 4. Analysis and Interpretation
# 
# The Deutsch‑Jozsa algorithm distinguishes constant from balanced functions with a **single query** to the oracle. Classically, this would require \( 2^{n-1} + 1 \) queries in the worst case. This exponential speedup is a hallmark of quantum computing.
# 
# - For a **constant oracle**, the measurement result is always `00...0` (all zeros), with probability 1.
# - For a **balanced oracle**, the measurement result is never `00...0`; at least one qubit will be in state |1⟩.
# 
# **Why does this work?**  
# The algorithm creates a superposition of all inputs and applies phase kickback from the oracle. The final Hadamard transform converts the phase information into a measurable pattern. If the function is constant, all amplitudes interfere constructively on the all‑zero state. If balanced, the all‑zero state has zero amplitude.
# 
# **Key takeaway:**  
# The Deutsch‑Jozsa algorithm demonstrates that quantum computers can solve certain problems exponentially faster than classical computers.


# ## Summary
# 
# **Accomplished:**
# - Implemented the Deutsch‑Jozsa algorithm for an arbitrary number of qubits.
# - Created constant and balanced oracles.
# - Visualised circuits and measurement histograms.
# - Verified that the algorithm correctly identifies constant and balanced functions.
# 
# **Key Insights:**
# - Quantum parallelism allows evaluating the function for all inputs simultaneously.
# - Phase kickback is the mechanism that encodes the function's global property.
# - The algorithm achieves exponential speedup over classical methods.
# 
# **Next Steps:**
# - Explore Grover's search algorithm for unstructured search.
# - Investigate the Quantum Fourier Transform and phase estimation.
# - Run the algorithm on real quantum hardware via IBM Quantum.