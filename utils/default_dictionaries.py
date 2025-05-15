from utils.config import atom_type1, atom_type2 
gen_lammps_input = {
    'units': 'metal',
    'dimension': 3,
    'boundary': 'p p p',
    'atom_style': 'atomic',
    'read_data': '"atoms_positions.data"',
    # "lattice": {"type": "fcc", "constant": 3.47},
    # "region": {"name": "whole", "type": "block", "bounds": [0, 6, 0, 6, 0, 6]},
    # "create_box": {"num_types": 1, "region": "whole"},
    # "create_atoms": {"num_type": 1, "region": "box"},
    'pair_style': 'meam',
    'pair_coeff': f'* * {atom_type1}{atom_type2}.library.meam {atom_type1} {atom_type2} {atom_type1}{atom_type2}.meam {atom_type1} {atom_type2}',
    'equilibration': {
        'reset_timestep': 0,
        'timestep': 0.005,
        'minimize': {'etol': 1e-6, 'ftol': 1e-8, 'maxiter': 10000, 'maxeval': 100000},
        'dump_min': {
            'filename': f'ideal_{atom_type1}{atom_type2}_bcc_B2.txt',
            'every': 10000,
            'attributes': 'id x y z',
            'modify': {'pbc': 'yes', 'sort': 'id'},
        },
        'dump_4a': {
            'filename': f'dump_{atom_type1}{atom_type2}_bcc_B2.*',
            'every': 500,
            'attributes': 'id type x y z fx fy fz', 
            'modify': {'pbc': 'yes', 'sort': 'id'},
        },
    },
    'md_settings': {
        'reset_timestep': 0,
        'velocity': {'all': {'create': [300, 12345], 'mom': 'yes', 'rot': 'no'}},
        'fix': {'id': 3, 'group': 'all', 'style': 'nvt', 'temp': [300.0, 300.0, 0.01]},
        'thermo': 500,
        'run': 2000,
    }
}

base_params_atoms_position = {
    'initial_temperature': 200,
    'initial_lattice_parameter': 2.81,#2.69
    'crystal_structure': "bcc",
    'system_size': 20,
    'index_atom_type_1': 1.0,
    'index_atom_type_2':2.0,
    'n_temp_variations': 5,#1,#6,
    'm_lattice_variations':40# 20 #20 add other 20 to be usable in birch-murnhaga
}

atomic_mass_atom_type1 = 58.6934 
atomic_mass_atom_type2 = 47.867
defect_percentages = [0.0005,0.001,0.005]#[0, 1,2,3]
vacancy_percentages = [0, 1, 2, 3, 4]
reduction_percentages = [-0.03,-0.02,-0.01,0.00,0.01,0.02,0.03]#[-0.02,-0.01, 0, 0.01,0.02]


# ------ Plots features
'''

In order to identify, sort each simulation in your graph, here you add the color, markes and linestyles that you will use, in this case i used, gradients colors, from lightskyblye to purple,etc.

'''
colors_plot = ['#00ffff', '#2ad5ff', '#55aaff', '#807fff', '#aa55ff', '#d52aff', '#ff00ff']
markers_plot = ['o', 's', '^', 'D', 'v', '<', '>']
linestyles_plot = ['-', '--', '-.', ':', '--', '-.'] 


# ------- Configurational entropy (Warren-Cowley parameters) calculation

nneigh=[0, 8, 14, 26, 50]

