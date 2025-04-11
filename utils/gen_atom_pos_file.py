def write_atoms_pos_file(new_filename, lattice_parameter, comp_1,comp_2, positions, atom_type_array, system_size, defect,atom_type1,atom_type2):
    """
    Writes a LAMMPS data file with atomic positions, system size, and lattice parameters.

    Parameters:
    - new_filename (str): Name of the output file.
    - lattice_parameter (float): Lattice parameter value.
    - composition (float): Composition of atom type 2.
    - positions (list of tuples): List of atomic positions [(x, y, z), ...].
    - atom_type_array (list of int): List of atom types corresponding to each position.
    - system_size (float): Scaling factor for defining simulation box dimensions.
    """
    with open(new_filename, 'w') as fdata:
        fdata.write(f'# lattice parameter {round(lattice_parameter, 2)} \n\n')
        fdata.write(f'# {atom_type1} composition {round(comp_1, 4)} \n\n')
        fdata.write(f'# {atom_type2} composition {round(comp_2, 4)} \n\n')
        fdata.write(f'# point defect  {defect}% \n\n')
        fdata.write(f'{len(positions)} atoms\n')
        fdata.write('2 atom types\n')
        fdata.write(f'0.0 {system_size * lattice_parameter} xlo xhi\n')
        fdata.write(f'0.0 {system_size * lattice_parameter} ylo yhi\n')
        fdata.write(f'0.0 {system_size * lattice_parameter} zlo zhi\n')
        fdata.write('\nAtoms\n\n')

        for i, pos in enumerate(positions):
            atom_type = int(atom_type_array[i])
            fdata.write(f'{i + 1} {atom_type} {pos[0]} {pos[1]} {pos[2]}\n')


