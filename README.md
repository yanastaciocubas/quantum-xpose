# Quantum Pose
### *Threat modeling and cryptographic analysis through quantum circuit simulation.*

---

## Overview

**Quantum Pose** is a research-oriented framework for simulating quantum-based cryptographic attacks and evaluating post-quantum defensive primitives. It provides executable circuit implementations of key quantum algorithms alongside a metrics layer for empirically comparing classical versus quantum computational complexity on real cryptographic problem instances.

---

## Motivation

RSA and ECC derive their security from the computational hardness of integer factorization and the discrete logarithm problem — both of which admit **polynomial-time quantum solutions**. As fault-tolerant quantum hardware approaches viability, the security margins of these schemes erode. Quantum Pose operationalizes this threat by running controlled simulations against reduced-parameter cryptographic instances, making the attack surface concrete and measurable.

---

## Core Modules

| Module | Description |
|--------|-------------|
| **Quantum Engine** | Circuit-level implementations of Shor's algorithm (order-finding via QFT + modular exponentiation), Grover's search (amplitude amplification with oracle injection), and standalone QFT benchmarks. Configurable qubit counts and noise models via Qiskit or Cirq. |
| **Attack Simulator** | Executes factorization and search attacks against small key instances (e.g. 8–16-bit RSA). Outputs asymptotic complexity comparisons: `O(n³)` classical vs. `O((log N)³)` quantum for Shor's; `O(√N)` Grover speedup over `O(N)` brute force. |
| **State Visualizer** | Renders amplitude probability distributions across the computational basis at each circuit layer — exposing interference patterns, phase kickback, and measurement collapse in real time. |
| **Metrics Dashboard** | Captures gate depth, T-count, circuit width, shot-averaged success probability, and simulated wall-clock time per run. Supports side-by-side regime comparison across problem sizes. |

---

## Post-Quantum Defense Layer

Alongside the attack surface, Quantum Pose simulates NIST PQC candidate schemes:

- **Lattice-based** (CRYSTALS-Kyber / NTRU) — hardness derived from Learning With Errors (LWE); resistant to Shor's
- **Hash-based signatures** (SPHINCS+) — stateless; security relies solely on hash function collision resistance
- **Code-based** (Classic McEliece) — hardness from syndrome decoding of random linear codes

Each scheme is benchmarked for key generation time, encapsulation/decapsulation latency, and ciphertext size relative to classical RSA/ECC at equivalent security levels.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Quantum Runtime | Qiskit (Aer simulator) or Cirq + `qsim` |
| Numerical Backend | NumPy, SciPy |
| Visualization | Matplotlib, Plotly |
| Frontend | Streamlit or Dash |
| Optional | TensorFlow Quantum for ML-based anomaly detection on quantum state fingerprints |

---

## Scope & Constraints

All simulations run on classical hardware via statevector or density-matrix simulation. Key sizes are intentionally limited (≤ 20 qubits) due to the `O(2ⁿ)` memory overhead of classical statevector simulation. Quantum Pose is designed as an **educational and analytical tool** — not a production cryptanalysis engine.