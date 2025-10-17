
import numpy as np
import matplotlib.pyplot as plt

def entropy_from_probs(p):
    p = np.clip(np.asarray(p), 1e-12, 1.0)
    return float(-np.sum(p * np.log2(p)))

def amplitude_bar(probabilities, title="Amplitudes"):
    fig, ax = plt.subplots(figsize=(6,3.6))
    ax.bar(range(len(probabilities)), probabilities)
    ax.set_xlabel("Basis state index")
    ax.set_ylabel("Probability")
    ax.set_title(title)
    fig.tight_layout()
    return fig

def line_plot(xs, ys, title, xlab, ylab):
    fig, ax = plt.subplots(figsize=(6,3.6))
    ax.plot(xs, ys)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_title(title)
    fig.tight_layout()
    return fig
