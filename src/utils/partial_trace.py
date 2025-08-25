from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace

def strip_measurements(qc: QuantumCircuit) -> QuantumCircuit:
    """
    Manually remove measurement instructions from a circuit.
    """
    new_qc = QuantumCircuit(qc.num_qubits)
    for instr, qargs, cargs in qc.data:
        if instr.name != "measure":
            new_qc.append(instr, qargs, cargs)
    return new_qc

def get_single_qubit_rhos(qc: QuantumCircuit):
    """
    Simulate a quantum circuit using Statevector and return reduced density matrices.
    """
    # Step 1: Remove measurements
    clean_qc = strip_measurements(qc)

    # Step 2: Simulate directly using Statevector
    statevector = Statevector.from_instruction(clean_qc)

    # Step 3: Partial trace for each qubit
    reduced_states = []
    for i in range(clean_qc.num_qubits):
        traced = partial_trace(statevector, [j for j in range(clean_qc.num_qubits) if j != i])
        reduced_states.append(traced)

    return reduced_states