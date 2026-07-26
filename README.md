# Quantum Computing: Algorithms and Implementations with Qiskit

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-green?logo=qiskit)](https://qiskit.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A production‑ready collection of notebooks and scripts covering foundational quantum algorithms – from qubits and gates to Deutsch‑Jozsa, Grover's search, Quantum Fourier Transform, and teleportation. Designed to showcase technical depth, reproducibility, and scientific rigor for proficiency in quantum computing, computational physics, and AI.**

---

## Overview

This repository contains **seven polished Jupyter notebooks** that systematically cover the fundamental algorithms of quantum computing using Qiskit. Each notebook follows a consistent, professional structure:

- **Clear narrative** – introduction, methodology, implementation, evaluation, and critical reflection.
- **Reproducibility** – fixed random seeds, self‑contained code, and no external file dependencies.
- **Modular code** – helper functions, docstrings, and PEP8 compliance.
- **Portfolio‑ready outputs** – circuit diagrams, statevectors, and histograms saved for inclusion in research portfolios.

The repository is designed to run in a Conda environment (`quantum_comp_env`) with Python 3.10. Dependencies include Qiskit, Qiskit‑Aer, and standard data science libraries – ensuring a clean, professional experience.

---

## Repository Structure

```text
QuantumComputing/
├── notebooks/ # Jupyter notebooks (original refactored versions)
│ ├── 01_IntroQuantumComputing.ipynb
│ ├── 02_EvenOdd_Parity.ipynb
│ ├── 03_DeutschJoszaAlgorithm.ipynb
│ ├── 04_GroverAlgorithm.ipynb
│ ├── 05_QuantumFourierTransform.ipynb
│ ├── 06_QuantumFourierTransform_Counter.ipynb
│ ├── 07_QuantumTeleportationQiskit.ipynb
│ └── *.png # Generated circuit diagrams and histograms
├── scripts/ # Python scripts exported from notebooks
│ ├── 01_IntroQuantumComputing.py
│ ├── 02_EvenOdd_Parity.py
│ ├── 03_DeutschJoszaAlgorithm.py
│ ├── 04_GroverAlgorithm.py
│ ├── 05_QuantumFourierTransform.py
│ ├── 06_QuantumFourierTransform_Counter.py
│ └── 07_QuantumTeleportationQiskit.py
├── README.md # This file
└── requirements.txt # Full dependency list for quantum_comp_env
```


---

## Notebooks Overview

### 01 – Introduction to Quantum Computing
**Topic:** Fundamentals of quantum circuits, qubits, gates, and simulation.  
**Content:** Single‑qubit gates (X, H, Z), superposition, multi‑qubit gates (CNOT), entanglement (Bell state), and statevector visualisation. Includes a two‑qubit circuit with swapped measurement and a teleportation preview.  
**Key Techniques:** `QuantumCircuit`, `AerSimulator`, `plot_histogram`, `plot_bloch_multivector`.  
**Visualisation:** Circuit diagrams, Bloch sphere, statevectors, histograms.  
**Applications:** Foundation for all subsequent quantum algorithms.

---

### 02 – Even/Odd Parity Checking
**Topic:** Simple quantum circuit to demonstrate superposition and measurement.  
**Content:** Two‑qubit circuit with Hadamard gates, an X gate, and measurement. Visualisation of the statevector and histogram.  
**Key Techniques:** Superposition, X gate, measurement.  
**Visualisation:** Circuit diagram, statevector, histogram.  
**Applications:** Understanding quantum measurement and probability.

---

### 03 – Deutsch‑Jozsa Algorithm
**Topic:** First quantum algorithm demonstrating exponential speedup over classical methods.  
**Content:** Constant and balanced oracles, phase kickback, quantum parallelism, and interpretation of results.  
**Key Techniques:** Oracle construction, Hadamard gates, phase kickback.  
**Visualisation:** Circuit diagrams, histograms for constant and balanced oracles.  
**Applications:** Function classification, understanding quantum advantage.

---

### 04 – Grover's Search Algorithm
**Topic:** Unstructured search algorithm with quadratic speedup.  
**Content:** Subset‑sum problem, phase oracle, diffusion operator (QFT‑based), amplitude amplification, and optimal iteration count.  
**Key Techniques:** Phase oracle, diffusion operator, amplitude amplification.  
**Visualisation:** Circuit diagram, histogram of measurement results.  
**Applications:** Search problems, optimisation, database search.

---

### 05 – Quantum Fourier Transform
**Topic:** Quantum analogue of the classical Discrete Fourier Transform.  
**Content:** Manual implementation of QFT and its inverse using Hadamard and controlled phase gates. Verification that QFT + inverse QFT = identity for numbers 0‑7.  
**Key Techniques:** Hadamard gates, controlled phase gates (CPhase), swaps.  
**Visualisation:** Circuit diagrams, histograms for each input number.  
**Applications:** Core building block for Shor's factoring and phase estimation.

---

### 06 – Quantum Fourier Transform (Counter Implementation)
**Topic:** Alternative implementation of QFT using a counter‑style loop.  
**Content:** QFT and inverse QFT with explicit register indexing, initialisation from a binary string, and optional swap to reverse qubit order.  
**Key Techniques:** `QuantumRegister`, `ClassicalRegister`, counter‑style loops.  
**Visualisation:** Circuit diagrams, histograms.  
**Applications:** Understanding different QFT implementations, phase estimation.

---

### 07 – Quantum Teleportation
**Topic:** Transfer of an unknown quantum state using entanglement and classical communication.  
**Content:** State preparation, Bell pair generation, basis change (CNOT + Hadamard), measurement, conditional X and Z gates, and verification of success.  
**Key Techniques:** Teleportation protocol, conditional operations (`if_test`), state initialisation, probability verification.  
**Visualisation:** Circuit diagram, comparison of input and output probabilities.  
**Applications:** Quantum communication, quantum networks, repeaters.

---

## Key Learnings and Insights

- **Qubits and gates** form the foundation of quantum circuits.
- **Superposition and entanglement** are the key resources that enable quantum advantage.
- **Deutsch‑Jozsa** demonstrates exponential speedup for a specific problem.
- **Grover's algorithm** provides a quadratic speedup for unstructured search.
- **Quantum Fourier Transform** is a core subroutine for many quantum algorithms (phase estimation, Shor's factoring).
- **Quantum teleportation** is a fundamental protocol for quantum communication and networking.
- **Reproducibility** is ensured through fixed random seeds, consistent simulation settings, and self‑contained code.

---

## Applications & Extensions

The techniques covered in this repository have direct applications in:

- **Cryptography** – Shor's factoring algorithm, quantum key distribution.
- **Optimisation** – Grover's search, quantum annealing.
- **Quantum Chemistry** – molecular simulation, phase estimation.
- **Quantum Machine Learning** – quantum kernels, variational quantum circuits.
- **Quantum Communication** – teleportation, quantum repeaters, entanglement distribution.

Each notebook can be easily extended to larger qubit counts, different oracles, or real hardware execution via IBM Quantum.