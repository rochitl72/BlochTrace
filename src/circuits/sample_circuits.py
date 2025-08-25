from qiskit import QuantumCircuit

def create_bell_ghz_circuit():
    """
    Creates a 3-qubit GHZ-like circuit: (|000⟩ + |111⟩) / √2
    """
    qc = QuantumCircuit(3)
    qc.h(0)          # Hadamard gate on qubit 0
    qc.cx(0, 1)      # CNOT gate from qubit 0 to 1
    qc.cx(1, 2)      # CNOT gate from qubit 1 to 2
    return qc