import numpy as np
import matplotlib.pyplot as plt
from qiskit.visualization.bloch import Bloch

def plot_bloch_sphere(rho, qubit_index):
    """
    Plots a single qubit's mixed state on a Bloch sphere.
    """
    # Compute Bloch vector from density matrix
    pauli_x = np.trace(rho.data @ np.array([[0, 1], [1, 0]])).real
    pauli_y = np.trace(rho.data @ np.array([[0, -1j], [1j, 0]])).real
    pauli_z = np.trace(rho.data @ np.array([[1, 0], [0, -1]])).real

    bloch_vector = [pauli_x, pauli_y, pauli_z]

    # Create Bloch sphere and render
    b = Bloch()
    b.add_vectors(bloch_vector)
    b.title = f"Qubit {qubit_index}"
    b.render()

    # Show the figure (Bloch renders internally)
    plt.show()