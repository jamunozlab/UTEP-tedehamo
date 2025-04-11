import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

'''
To ensure the accuracy and reliability of the results, multiple experiments are conducted, each covering different ranges of temperature,
defect concentrations, and volumes. In other words, a high-throughput set of molecular dynamics (MD) simulations is generated.
For each simulation, data obtained from the Birch-Murnaghan equation of state fit are collected and stored in this file.
These data will then be organized, plotted, and used to produce figures representing key mechanical properties, 
including the lattice parameter, bulk modulus, and internal energy. Before organizing the results,
an average is computed for each mechanical property. For instance, 
the average bulk modulus is calculated as:

B_p = frac{1}{n} sum_{i=1}^{n} B_i

where n  is the number of simulations and B_i is the bulk modulus from the i-th simulation. Additionally, 
the uncertainties associated with each property are estimated through error propagation
to provide a robust statistical analysis of the results.
sigma_{B} = sqrt(sum_{i=1}^{n} B_{error_i})
'''

def extract_data(input_files):
    bulk_modulus       = []
    lattice_par        = []
    bulk_modulus_error = []
    lattice_par_error  = []
    inter_energy       = []
    inter_energy_error = []
    volume             = []
    volume_error       = []
    bulk_mod_prim      = []
    bulk_mod_prim_error= []
    
    for input_path in input_files:
        try:
            df = pd.read_csv(input_path)
            
            if 'Value' in df.columns and 'Error' in df.columns:
                inter_energy.append(df['Value'][0])
                inter_energy_error.append(df['Error'][0])
                volume.append(df['Value'][1])
                volume_error.append(df['Error'][1])
                bulk_modulus.append(df['Value'][2])
                bulk_modulus_error.append(df['Error'][2])
                bulk_mod_prim.append(df['Value'][3])
                bulk_mod_prim_error.append(df['Error'][3])
                lattice_par.append(df['Value'][4])
                lattice_par_error.append(df['Error'][4])
            else:
                print(f"Columns 'Value' and 'Error' not found in {input_path}")
        except FileNotFoundError:
            print(f"File not found: {input_path}")
        except Exception as e:
            print(f"Error reading {input_path}: {e}")

    return (
        inter_energy, inter_energy_error, volume, volume_error,
        bulk_modulus, bulk_modulus_error, bulk_mod_prim, bulk_mod_prim_error,
        lattice_par, lattice_par_error
    )
def calculate_mean(*datasets):
    n = len(datasets)
    return [sum(values) / n for values in zip(*datasets)]

def calculate_propagated_error(*errors):
    return [np.sqrt(sum(e**2 for e in values)) for values in zip(*errors)]

def combine_and_average(simulation_data_dicts, temperature):
    """
    simulation_data_dicts: list of dictionaries, one per simulation (e.g. [input_files_sim1, input_files_sim2, ...])
    temperature: temperature key to extract from each dictionary
    """

    extracted = [extract_data(sim_dict[temperature]) for sim_dict in simulation_data_dicts]
    
    # Unpack the data by category (0: inter_energy, 1: error_inter_energy, ...)
    data_by_index = list(zip(*extracted))  # Each element is a list of values from all simulations for one property

    return {
        'inter_energy_mean': calculate_mean(*data_by_index[0]),
        'inter_energy_error_propagated': calculate_propagated_error(*data_by_index[1]),
        'volume_mean': calculate_mean(*data_by_index[2]),
        'volume_error_propagated': calculate_propagated_error(*data_by_index[3]),
        'bulk_modulus_mean': calculate_mean(*data_by_index[4]),
        'bulk_modulus_error_propagated': calculate_propagated_error(*data_by_index[5]),
        'bulk_mod_prim_mean': calculate_mean(*data_by_index[6]),
        'bulk_mod_prim_error_propagated': calculate_propagated_error(*data_by_index[7]),
        'lattice_par_mean': calculate_mean(*data_by_index[8]),
        'lattice_par_error_propagated': calculate_propagated_error(*data_by_index[9])
    }


def csv_gen_before_thermal(df,i,atom_type1,atom_type2):
    # Renaming columns
    rename = {
        'inter_energy_mean': f'internal_energy_{i}K_ord',
        'inter_energy_error_propagated': f'internal_energy_{i}K_ord_error',
        'bulk_modulus_mean': f'bulk_modulus_{i}K_ord',
        'bulk_modulus_error_propagated': f'bulk_modulus_{i}K_ord_error',
        'bulk_mod_prim_mean': f'bulk_modulus_derivative_{i}K_ord',
        'bulk_mod_prim_error_propagated': f'bulk_modulus_derivative_{i}K_ord_error',
        'lattice_par_mean': f'lattice_parameter_{i}K_ord',
        'lattice_par_error_propagated': f'lattice_parameter_{i}K_ord_error'
    }
    
    df.rename(columns=rename, inplace=True)
    
    try:
        df[f'bulk_modulus_{i}K_ord_up'] = df[f'bulk_modulus_{i}K_ord'] + df[f'bulk_modulus_{i}K_ord_error']
        df[f'bulk_modulus_{i}K_ord_down'] = df[f'bulk_modulus_{i}K_ord'] - df[f'bulk_modulus_{i}K_ord_error']
        df[f'bulk_modulus_derivative_{i}K_ord_up'] = df[f'bulk_modulus_derivative_{i}K_ord'] + df[f'bulk_modulus_derivative_{i}K_ord_error']
        df[f'bulk_modulus_derivative_{i}K_ord_down'] = df[f'bulk_modulus_derivative_{i}K_ord'] - df[f'bulk_modulus_derivative_{i}K_ord_error']
    except KeyError as e:
        print(f"Column missing: {e}")

    df.drop(columns=['volume_mean', 'volume_error_propagated'], axis=1, inplace=True)
    
    df.insert(0, f'{atom_type1}_composition', Ni_comp)
    df.insert(1, f'{atom_type2}_composition', Ti_comp)
    
    columns_order = list(df.columns)

    columns_order.remove(f'bulk_modulus_{i}K_ord_up')
    columns_order.remove(f'bulk_modulus_{i}K_ord_down')
    columns_order.remove(f'bulk_modulus_derivative_{i}K_ord_up')
    columns_order.remove(f'bulk_modulus_derivative_{i}K_ord_down')

    columns_order.insert(6, f'bulk_modulus_{i}K_ord_up')
    columns_order.insert(7, f'bulk_modulus_{i}K_ord_down')
    columns_order.insert(10, f'bulk_modulus_derivative_{i}K_ord_up')
    columns_order.insert(11, f'bulk_modulus_derivative_{i}K_ord_down')

    df = df[columns_order]

    return df
    