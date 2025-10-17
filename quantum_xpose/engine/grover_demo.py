
import time
import numpy as np
from typing import Dict, Any, Tuple

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Minimal oracle: mark a single basis state |target>
def mark_oracle(n_qubits: int, target: int) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits)
    # Flip to |target> by applying X on 0-bits, then reflect phase on |11..1|, then uncompute.
    target_bits = [(target >> i) & 1 for i in range(n_qubits)]
    for i, b in enumerate(target_bits[::-1]):
        if b == 0:
            qc.x(i)
    # multi-controlled Z on |11..1>
    qc.h(n_qubits-1)
    if n_qubits == 1:
        qc.z(0)
    else:
        qc.mcp(np.pi, list(range(n_qubits-1)), n_qubits-1)
    qc.h(n_qubits-1)
    for i, b in enumerate(target_bits[::-1]):
        if b == 0:
            qc.x(i)
    return qc

def diffuser(n_qubits: int) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    qc.h(n_qubits-1)
    if n_qubits == 1:
        qc.z(0)
    else:
        qc.mcp(np.pi, list(range(n_qubits-1)), n_qubits-1)  # multi-controlled Z
    qc.h(n_qubits-1)
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))
    return qc

def grover_statevector(n_qubits: int, target: int, iterations: int) -> Tuple[Statevector, Dict[str, Any]]:
    # Start in uniform superposition
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    sv = Statevector.from_instruction(qc)

    oracle = mark_oracle(n_qubits, target)
    diff = diffuser(n_qubits)

    t0 = time.time()
    for _ in range(iterations):
        sv = sv.evolve(oracle)
        sv = sv.evolve(diff)
    elapsed = time.time() - t0

    probs = sv.probabilities()
    success_prob = probs[target] if target < len(probs) else 0.0
    info = {"runtime_sec": elapsed, "success_prob": float(success_prob)}
    return sv, info
