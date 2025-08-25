import sys
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
from qiskit import QuantumCircuit

# Local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.circuits.sample_circuits import create_bell_ghz_circuit
from src.utils.partial_trace import get_single_qubit_rhos

# ----------------------------
# Plotly Bloch Sphere Function
# ----------------------------
def plotly_bloch_sphere(bloch_vector, qubit_index):
    x, y, z = bloch_vector
    fig = go.Figure()

    # Draw Bloch sphere surface
    u, v = np.mgrid[0:2 * np.pi:100j, 0:np.pi:100j]
    xs = np.cos(u) * np.sin(v)
    ys = np.sin(u) * np.sin(v)
    zs = np.cos(v)
    fig.add_trace(go.Surface(x=xs, y=ys, z=zs, opacity=0.1, colorscale='Blues'))

    # Bloch vector arrow
    fig.add_trace(go.Cone(
        x=[0], y=[0], z=[0],
        u=[x], v=[y], w=[z],
        colorscale="Reds",
        sizemode="absolute",
        sizeref=0.3,
        anchor="tail"
    ))

    fig.update_layout(
        title=f"🧭 Bloch Sphere - Qubit {qubit_index}",
        scene=dict(
            xaxis=dict(range=[-1, 1]),
            yaxis=dict(range=[-1, 1]),
            zaxis=dict(range=[-1, 1]),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )
    return fig

# ----------------------------
# Streamlit UI Setup
# ----------------------------
st.set_page_config(page_title="BlochTrace", layout="wide")
st.title("🌀 BlochTrace: Quantum Circuit Visualizer")

# --- Sidebar ---
st.sidebar.header("📌 Navigation")
page = st.sidebar.radio("Go to", ["Upload QASM", "View Circuit", "Density Matrices", "Bloch Spheres"])

# --- Global State Initialization ---
if "qc" not in st.session_state:
    st.session_state.qc = create_bell_ghz_circuit()
    st.session_state.reduced_states = get_single_qubit_rhos(st.session_state.qc)

# ----------------------------
# Upload QASM Page
# ----------------------------
if page == "Upload QASM":
    st.subheader("📁 Upload Quantum Circuit (.qasm)")
    uploaded_file = st.file_uploader("Upload a `.qasm` file", type=["qasm"])

    if uploaded_file:
        qasm_str = uploaded_file.read().decode("utf-8")

        # Save uploaded QASM with timestamp
        os.makedirs("uploaded_qasm", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"uploaded_qasm/{timestamp}_{uploaded_file.name}"
        with open(save_path, "w") as f:
            f.write(qasm_str)

        # Load and store circuit
        qc = QuantumCircuit.from_qasm_str(qasm_str)
        st.session_state.qc = qc
        st.session_state.reduced_states = get_single_qubit_rhos(qc)

        st.success(f"✅ Circuit loaded and saved as `{save_path}`")
    else:
        st.info("Using built-in GHZ 3-qubit circuit as fallback.")

# ----------------------------
# Circuit Visualization Page
# ----------------------------
elif page == "View Circuit":
    st.subheader("🧪 Quantum Circuit Diagram")

    # Resize and format the figure before display
    fig, ax = plt.subplots(figsize=(6, 2))  # Custom size
    circuit_draw = st.session_state.qc.draw(output="mpl", style="iqp")
    plt.tight_layout()

    # Center the circuit using columns
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.pyplot(circuit_draw)

# ----------------------------
# Density Matrices Page
# ----------------------------
elif page == "Density Matrices":
    st.subheader("🔬 Single-Qubit Reduced Density Matrices")
    for idx, rho in enumerate(st.session_state.reduced_states):
        st.markdown(f"**Qubit {idx}**:")
        st.text(rho)

# ----------------------------
# Bloch Spheres Page
# ----------------------------
elif page == "Bloch Spheres":
    st.subheader("🌐 Interactive Bloch Sphere Visualization")
    for idx, rho in enumerate(st.session_state.reduced_states):
        st.markdown(f"**Qubit {idx}**:")

        # Compute Bloch vector
        pauli_x = np.trace(rho.data @ np.array([[0, 1], [1, 0]])).real
        pauli_y = np.trace(rho.data @ np.array([[0, -1j], [1j, 0]])).real
        pauli_z = np.trace(rho.data @ np.array([[1, 0], [0, -1]])).real
        bloch_vector = [pauli_x, pauli_y, pauli_z]

        # Plot using Plotly
        st.plotly_chart(plotly_bloch_sphere(bloch_vector, idx), use_container_width=True)