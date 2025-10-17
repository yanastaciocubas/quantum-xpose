
import time
from typing import Optional, Tuple

def classical_factor(n: int) -> Tuple[Optional[int], Optional[int]]:
    # Tiny classical fallback; not efficient, for demo only
    if n < 2:
        return (None, None)
    p = 2
    while p*p <= n:
        if n % p == 0:
            return (p, n//p)
        p += 1
    return (None, None)

def shor_factor(n: int):
    '''
    Attempt to use Qiskit's Shor if available; otherwise return a stub with guidance.
    Returns: dict with keys: 'ok', 'p', 'q', 'used_shor', 'message', 'runtime_sec'
    '''
    t0 = time.time()
    try:
        # Some environments ship Shor in qiskit_algorithms (separate) rather than qiskit.algorithms
        from qiskit_algorithms import Shor  # optional; may not exist
        shor = Shor()
        result = shor.factorize(n)
        elapsed = time.time() - t0
        if getattr(result, 'factors', None):
            p, q = result.factors[0]
            return {"ok": True, "p": int(p), "q": int(q), "used_shor": True, "message": "Quantum Shor succeeded.", "runtime_sec": elapsed}
        return {"ok": False, "p": None, "q": None, "used_shor": True, "message": "Shor returned no factors.", "runtime_sec": elapsed}
    except Exception as e:
        # Fallback: classical and guidance
        p, q = classical_factor(n)
        elapsed = time.time() - t0
        msg = ("Qiskit Shor not available. Install `qiskit-algorithms` to enable the true Shor demo. "
               "Falling back to classical trial-division so you can still see the end-to-end flow.")
        return {"ok": (p is not None), "p": p, "q": q, "used_shor": False, "message": msg, "runtime_sec": elapsed}
