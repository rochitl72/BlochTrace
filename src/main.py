from circuits.sample_circuits import create_bell_ghz_circuit
from utils.partial_trace import get_single_qubit_rhos
from visuals.bloch_plot import plot_bloch_sphere

def main():
    print("\n🎯 Building Quantum Circuit...")
    qc = create_bell_ghz_circuit()
    print(qc.draw())

    print("\n🧠 Getting Single-Qubit Reduced Density Matrices...")
    reduced_states = get_single_qubit_rhos(qc)

    for idx, rho in enumerate(reduced_states):
        print(f"\n🔬 Qubit {idx} Reduced Density Matrix:")
        print(rho)

    print("\n🧭 Plotting Bloch Spheres...")
    for idx, rho in enumerate(reduced_states):
        plot_bloch_sphere(rho, idx)

if __name__ == "__main__":
    main()