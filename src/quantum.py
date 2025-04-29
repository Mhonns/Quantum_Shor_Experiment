import numpy as np
from math import gcd
import fractions
from qiskit import QuantumCircuit, execute
from qiskit_aer import Aer

n_target_wires = 8  # Number of qubits for the target register
n_estimation_wires = 12  # Number of qubits for phase estimation


# Utility functions
def is_coprime(a, N):
    """Check if a and N are coprime."""
    return gcd(a, N) == 1


def is_odd(r):
    """Check if the period r is odd."""
    return r % 2 == 1


def is_not_one(x, N):
    """Check if x is not congruent to 1 modulo N."""
    return (x % N) != 1


def get_matrix_a_mod_N(a, N):
    """Build the unitary matrix for modular multiplication a mod N."""
    dim = 2 ** n_target_wires
    U = np.zeros((dim, dim), dtype=complex)
    for x in range(dim):
        if x < N:
            y = (a * x) % N
        else:
            y = x
        U[y, x] = 1
    return U


def qpe_circuit(matrix, n_target_wires, n_estimation_wires):
    """Construct the Quantum Phase Estimation circuit."""
    qc = QuantumCircuit(n_target_wires + n_estimation_wires, n_estimation_wires)

    # Prepare the target register in |1> state
    qc.x(0)

    # Apply Hadamard gates to the estimation qubits
    for wire in range(n_target_wires, n_target_wires + n_estimation_wires):
        qc.h(wire)

    # Apply controlled unitaries
    for idx in range(n_estimation_wires):
        unitary_power = 2 ** idx
        U = matrix
        for _ in range(unitary_power - 1):
            U = np.dot(U, matrix)
        # Create a gate from the matrix and apply it as a controlled operation
        gate = QuantumCircuit(n_target_wires)
        gate.unitary(U, range(n_target_wires))
        controlled_gate = gate.control()
        qc.append(controlled_gate, [n_target_wires + idx] + list(range(n_target_wires)))

    # Apply the inverse Quantum Fourier Transform (QFT)
    for j in range(n_estimation_wires - 1, -1, -1):
        qc.h(n_target_wires + j)
        for m in range(j):
            angle = -np.pi / (2 ** (j - m))
            qc.cp(angle, n_target_wires + j, n_target_wires + m)

    # Measure the estimation qubits
    qc.measure(range(n_target_wires, n_target_wires + n_estimation_wires), range(n_estimation_wires))

    return qc


def get_phase(qc, backend, n_estimation_wires):
    """Estimate the phase from the QPE circuit."""
    job = execute(qc, backend, shots=1)
    result = job.result()
    sample = list(result.get_counts().keys())[0]
    decimal = int(sample, 2)
    phase = decimal / (2 ** n_estimation_wires)
    return phase


def get_period(matrix, backend):
    """Estimate the period using multiple shots of phase estimation."""
    shots = 10
    periods = []
    for _ in range(shots):
        qc = qpe_circuit(matrix, n_target_wires, n_estimation_wires)
        phase = get_phase(qc, backend, n_estimation_wires)
        fraction = fractions.Fraction(phase).limit_denominator(2 ** n_estimation_wires)
        periods.append(fraction.denominator)
    return max(periods)


def shor(N):
    """Run Shor's algorithm to find factors of N."""
    backend = Aer.get_backend('qasm_simulator')
    for a in range(2, N - 1):
        if not is_coprime(a, N):
            p = gcd(a, N)
            q = N // p
            break
        else:
            U_na = get_matrix_a_mod_N(a, N)
            r = get_period(U_na, backend)
            if not is_odd(r):
                x = pow(a, r // 2, N)
                if is_not_one(x, N):
                    p = gcd(x - 1, N)
                    q = gcd(x + 1, N)
                    if p * q == N and p != 1 and q != 1:
                        break
    return [p, q]


# Run the algorithm
test_numbers = [
    15,  # 3 * 5
    15,  # 3 * 5
    15,  # 3 * 5
    21,  # 3 * 7
    21,  # 3 * 7
    21,  # 3 * 7
]

for N in test_numbers:
    factors = shor(N)
    print("Factors of", N, "are:", factors)