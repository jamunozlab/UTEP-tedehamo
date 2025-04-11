import os
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from lmfit import Model
from utils.config import atom_type1, atom_type2
from utils.default_dictionaries import base_params_atoms_position

total_num_atoms = 2 * base_params_atoms_position['system_size'] **3 
def E_BM(V, E0, V0, B0, B0p):
    return E0 + (9/16) * V0 * B0 * ((B0p * ((V0/V)**(2/3) - 1 )**3) + (((V0/V)**(2/3) - 1 )**2) * (6 - 4 * ((V0/V)**(2/3))))

def E_M(V, E0, V0, B0, B0p):
    return E0 + B0 * V0 * ((1/(B0p * (B0p - 1))) * ((V / V0)**(1 - B0p)) + (V / (B0p * V0)) - (1 / (B0p - 1)))

def Birch_Murnaghan_fit(simulations_path, reduction_percentages, defect_percentages, base_params_atoms_position):
    for conc in reduction_percentages:
        concentration_path_sim = os.path.join(simulations_path, f'{(0.50-conc):.2f}-{atom_type1}-{(0.50+conc):.2f}-{atom_type2}')
        for defect in defect_percentages:
            defect_path_sim = os.path.join(concentration_path_sim, f'defect_{defect}%')
            for temperature_variation in range(base_params_atoms_position['n_temp_variations']):
                temperature = temperature_variation * 100 + base_params_atoms_position['initial_temperature']
                base_directory = os.path.join(defect_path_sim, f'{temperature}K')
                
                simulation_1 = pd.read_excel(os.path.join(base_directory, f'Lattice_vs_Energy {atom_type1}{(0.50-conc):.2f}{atom_type2}{(0.50+conc):.2f} - 1000 timesteps.xlsx'))
                simulation_2 = pd.read_excel(os.path.join(base_directory,  f'Lattice_vs_Energy {atom_type1}{(0.50-conc):.2f}{atom_type2}{(0.50+conc):.2f} - 1500 timesteps.xlsx'))
                
                X = np.vstack([simulation_1['Lattice Parameter'].values.reshape(-1, 1), 
                               simulation_2['Lattice Parameter'].values.reshape(-1, 1)])
                E = np.vstack([simulation_1['Energy'].values.reshape(-1, 1), 
                               simulation_2['Energy'].values.reshape(-1, 1)]) / total_num_atoms
                V = X ** 3
                
                gmodel = Model(E_M)
                result = gmodel.fit(E, V=V, E0=-4, V0=20, B0=140, B0p=-4, nan_policy='omit')
                
                param_array = np.zeros([5, 2])
                indexes = []
                i = 0
                for parname, par in result.params.items():
                    indexes.append(parname)
                    param_array[i, 0] = par.value
                    param_array[i, 1] = par.stderr
                    i += 1
                param_array[2, :] = param_array[2, :] * 160.2 * math.sqrt(2)
                lattice_val = (param_array[1, 0]) ** (1/3)
                lattice_error = ((param_array[1, 0] + param_array[1, 1]) ** (1/3) - (param_array[1, 0] - param_array[1, 1]) ** (1/3)) / 2
                param_array[i, 0] = lattice_val
                param_array[i, 1] = lattice_error
                indexes.append('L0')
                
                df_param_array = pd.DataFrame(param_array, index=indexes, columns=['Value', 'Error'])
                df_param_array.to_csv(os.path.join(base_directory, f'Errors_and_Parameters Birch Murnaghan {(0.50-conc):.2f}-{(0.50+conc):.2f}.csv'))
                
                params = result.best_values
                volumes = np.linspace(int(math.floor(V[0])), int(math.floor(V[-1]) + 3), num=50)
                ens = [E_M(v, params['E0'], params['V0'], params['B0'], params['B0p']) for v in volumes]
                
                plt.plot(V, E, 'bo')
                plt.plot(volumes, ens)
                plt.title(f'Birch-Murnaghan Fit at composition {(0.50-conc):.2f}-{atom_type1} {(0.50+conc):.2f}-{atom_type2}')
                plt.xlabel(r'Volume ($\mathrm{\AA}^3$)')
                plt.ylabel('Internal Energy (eV)')
                
                param_text = fr"$E_0={params['E0']:.2f}, V_0={params['V0']:.2f}, B_0={params['B0'] * 160.2 * math.sqrt(2):.2f}, B'_0={params['B0p']:.2f}$"
                descrip_graph1 = f'Point Defect: {defect}%'
                descrip_graph2 = f'Temperature: {temperature}K'
                plt.text(0.1, 0.95, param_text, fontsize=13.5, transform=plt.gca().transAxes, verticalalignment='top')
                plt.text(0.25, 0.85, descrip_graph1, fontsize=13.5, transform=plt.gca().transAxes, verticalalignment='top')
                plt.text(0.3, 0.75, descrip_graph2, fontsize=13.5, transform=plt.gca().transAxes, verticalalignment='top')
                plt.show()
