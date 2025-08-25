OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];

// Apply different single-qubit gates to each qubit
h q[0];         // Qubit 0: Hadamard → vector on equator (x-direction)
x q[1];         // Qubit 1: Pauli-X → vector pointing along -z axis
ry(1.0) q[2];   // Qubit 2: Rotation around y-axis → diagonal vector