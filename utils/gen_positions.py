import numpy as np
def generate_atomic_positions(lattice_parameters, system_size):
    """
    Generates atomic positions for  body center cubic system with given lattice parameters.

    Parameters:
    lattice_parameters (list or np.array): List of lattice parameters to iterate over.
    system_size (int): The size of the system in terms of unit cells along each dimension.

    Returns:
    dict: A dictionary where keys are lattice parameters and values are lists of atomic positions.
    """
    atomic_positions = {}

    for lattice_parameter in lattice_parameters:
        basis = np.array([[1, 0.0, 0.0],
                          [0.0, 1, 0.0],
                          [0.0, 0.0, 1]]) * lattice_parameter

        base_atoms = np.array([[0.0, 0.0, 0.0],
                               [0.5, 0.5, 0.5]]) * lattice_parameter

        positions = []
        for i in range(system_size):
            for j in range(system_size):
                for k in range(system_size):
                    base_position = np.array([i, j, k])
                    cart_position = np.dot(basis.T, base_position)
                    for atom in base_atoms:
                        positions.append(cart_position + atom)

        atomic_positions[lattice_parameter] = positions

    return atomic_positions