import streamlit as st
import numpy as np

from quantum_xpose.engine.grover_demo import grover_statevector
from quantum_xpose.engine.shor_demo import shor_factor
from quantum_xpose.viz.plots import amplitude_bar, entropy_from_probs, line_plot
from quantum_xpose.metrics.bench import time_call

st.set_page_config(page_title="Quantum Xpose — Security Demos", layout="wide")

st.title("Quantum Xpose")
st.caption("Exposing hidden threats through the lens of quantum security")

tab1, tab2, tab3, tab4 = st.tabs(["Grover (search)", "QFT view", "Shor (factor)", "Metrics"])

with tab1:
    st.header("Grover's Algorithm: password search toy")
    c1, c2 = st.columns([1,1])
    with c1:
        n_qubits = st.slider("Number of qubits (2–8)", 2, 8, 3)
        N = 2**n_qubits
        target = st.number_input(f"Secret index (0–{N-1})", min_value=0, max_value=N-1, value=min(3, N-1), step=1)
        iters = st.slider("Grover iterations", 0, min(20, 2*N), max(1, int(np.floor(np.pi/4*np.sqrt(N)))))
        run = st.button("Run Grover")
    if run:
        sv, info = grover_statevector(n_qubits, target, iters)
        probs = sv.probabilities()
        ent = entropy_from_probs(probs)
        st.write(f"**Success probability for target {target}:** {info['success_prob']:.3f}")
        st.write(f"**Runtime (sec):** {info['runtime_sec']:.4f}  •  **Entropy (bits):** {ent:.3f}")
        st.pyplot(amplitude_bar(probs, title="Probability distribution after Grover"))

with tab2:
    st.header("QFT:simple amplitude view")
    st.write("Apply the Quantum Fourier Transform idea on a basic input distribution to see spreading/concentration.")
    n = st.slider("Number of states (power-of-two)", 4, 64, 8, step=4)
    mode = st.selectbox("Input pattern", ["delta at 0", "two spikes", "random"])
    rng = np.random.default_rng(0)
    probs = np.zeros(n, dtype=float)
    if mode == "delta at 0":
        probs[0] = 1.0
    elif mode == "two spikes":
        probs[0] = 0.5; probs[n//2] = 0.5
    else:
        x = rng.random(n)
        probs = x / x.sum()
    st.pyplot(amplitude_bar(probs, title="Input distribution"))

    # "QFT-like" effect via unitary DFT on amplitudes (toy)
    amps = np.sqrt(probs) * np.exp(1j*0)  # assume real non-negative amplitudes
    # DFT
    F = np.fft.fft(np.eye(n)) / np.sqrt(n)
    out_amps = F @ amps
    out_probs = np.abs(out_amps)**2
    st.pyplot(amplitude_bar(out_probs, title="After (toy) QFT/DFT"))

    st.write(f"Entropy in: **{entropy_from_probs(probs):.3f}** bits  •  out: **{entropy_from_probs(out_probs):.3f}** bits")

with tab3:
    st.header("Shor:factor a small integer")
    N = st.number_input("Composite N (try 15, 21, 33...)", min_value=2, value=15, step=1)
    if st.button("Factor N"):
        res = shor_factor(int(N))
        used = "Quantum Shor" if res["used_shor"] else "Classical fallback"
        st.write(f"**Method:** {used}")
        st.write(f"**Message:** {res['message']}")
        st.write(f"**Runtime (sec):** {res['runtime_sec']:.4f}")
        if res["ok"]:
            st.success(f"Factors: {res['p']} × {res['q']} = {int(N)}")
        else:
            st.warning("No factors found (is N prime or algorithm unavailable?).")
    st.info("Note: Real Shor may require installing `qiskit-algorithms`. This demo tries to import it; otherwise it falls back.")

with tab4:
    st.header("Metrics: compare classical vs quantum toy scale")
    st.write("Rough, teaching-scale comparisons. For Grover, runtime is iterations; classical is linear scan.")
    max_n_qubits = st.slider("Max qubits (Grover)", 2, 10, 8)
    xs = list(range(2, max_n_qubits+1))
    classical = [2**q for q in xs]
    quantum = [int(np.floor(np.pi/4*np.sqrt(2**q))) for q in xs]
    st.pyplot(line_plot(xs, classical, "Classical steps (linear)", "qubits", "steps"))
    st.pyplot(line_plot(xs, quantum, "Grover steps (√N)", "qubits", "steps"))
    st.caption("For Shor, asymptotically poly(log N) on ideal quantum hardware, versus sub-exponential/classical best-known. This dashboard focuses on Grover due to simulator practicality.")
