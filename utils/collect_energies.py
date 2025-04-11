from utils.config import simulations_path, atom_type1, atom_type2
from utils.default_dictionaries import base_params_atoms_position, defect_percentages, reduction_percentages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def extracting_energies_before_BM():
    """
    Processes simulation data by extracting energy values at 1000 and 1500 timesteps, 
    fitting polynomial regression, finding the minimum energy and lattice parameter, 
    generating plots for both timesteps, and saving results in Excel files.
    """
    
    lattice_parameters = [
        base_params_atoms_position['initial_lattice_parameter'] + i * 0.01 
        for i in range(base_params_atoms_position['m_lattice_variations'])
    ]

    for conc in reduction_percentages:
        concentration_path_sim = os.path.join(simulations_path, f'{(0.50-conc):.2f}-{atom_type1}-{(0.50+conc):.2f}-{atom_type2}')

        for defect in defect_percentages:
            defect_path_sim = os.path.join(concentration_path_sim, f'defect_{defect}%')

            for temperature_variation in range(base_params_atoms_position['n_temp_variations']):
                temperature = temperature_variation * 100 + base_params_atoms_position['initial_temperature']
                energies_array_1000 = np.empty((0, 2))
                energies_array_1500 = np.empty((0, 2))

                for lattice_parameter in lattice_parameters:
                    directory = os.path.join(defect_path_sim, f'{atom_type1}{atom_type2}_T_{temperature}_L_{lattice_parameter:.2f}')
                    temp_dir = f'{temperature}K'

                    file_path = os.path.join(directory, 'output.txt')

                    # -------- Extracting energies
                    try:
                        with open(file_path, 'r') as f:
                            lines = f.readlines()

                        if len(lines) < 86:
                            print(f"Warning: File {file_path} does not contain enough lines.")
                            continue

                        initial_pe_1000 = lines[84].strip().split()
                        initial_pe_1500 = lines[85].strip().split()

                        if len(initial_pe_1000) >= 5 and len(initial_pe_1500) >= 5:
                            energy_1000 = float(initial_pe_1000[4])
                            energy_1500 = float(initial_pe_1500[4])
                        else:
                            print(f"Warning: Simulation might not have been performed correctly in {file_path}.")
                            continue

                        # -------- Collecting both energies
                        energies_array_1000 = np.vstack([energies_array_1000, [round(lattice_parameter, 2), energy_1000]])
                        energies_array_1500 = np.vstack([energies_array_1500, [round(lattice_parameter, 2), energy_1500]])

                    except FileNotFoundError:
                        print(f"Error: File {file_path} not found.")
                        continue
                    except ValueError:
                        print(f"Error: Could not convert energy value to float in {file_path}.")
                        continue
                    except Exception as e:
                        print(f"Unexpected error while processing {file_path}: {e}")
                        continue

                if energies_array_1000.shape[0] == 0 or energies_array_1500.shape[0] == 0:
                    print(f"Skipping {defect_path_sim}/{temp_dir} due to missing energy data.")
                    continue

                # -------- Polynomial regression for both 1000 and 1500 timesteps
                model_1000 = np.poly1d(np.polyfit(energies_array_1000[:, 0], energies_array_1000[:, 1], 20))
                model_1500 = np.poly1d(np.polyfit(energies_array_1500[:, 0], energies_array_1500[:, 1], 20))

                lattices_linspace = np.linspace(lattice_parameters[0], lattice_parameters[-1], 500).reshape(-1, 1)

                energies_regression_1000 = np.hstack([lattices_linspace, model_1000(lattices_linspace).reshape(-1, 1)])
                min_energy_1000 = np.min(energies_regression_1000[:, 1])
                min_lattice_1000 = lattices_linspace[np.argmin(energies_regression_1000[:, 1])][0]

                energies_regression_1500 = np.hstack([lattices_linspace, model_1500(lattices_linspace).reshape(-1, 1)])
                min_energy_1500 = np.min(energies_regression_1500[:, 1])
                min_lattice_1500 = lattices_linspace[np.argmin(energies_regression_1500[:, 1])][0]

                # -------- Plot results for both 1000 and 1500 timesteps
                props = dict(boxstyle='round', facecolor='white', edgecolor='gray', alpha=0.5)
                fig, ax = plt.subplots()
                plt.plot(energies_regression_1000[:, 0], energies_regression_1000[:, 1], label='Regression Line (1000 ts)')
                plt.plot(energies_regression_1500[:, 0], energies_regression_1500[:, 1], label='Regression Line (1500 ts)')
                plt.scatter(energies_array_1000[:, 0], energies_array_1000[:, 1], label='Simulations Data (1000 ts)', s=10)
                plt.scatter(energies_array_1500[:, 0], energies_array_1500[:, 1], label='Simulations Data (1500 ts)', s=10)

                ax.text(0.69, 0.80, f'Minimum Lattice (1000 ts): \n {round(min_lattice_1000, 6)}',
                        transform=ax.transAxes, verticalalignment='top', bbox=props)
                ax.text(0.69, 0.67, f'Minimum Energy (1000 ts): \n {round(min_energy_1000, 6)}',
                        transform=ax.transAxes, verticalalignment='top', bbox=props)
                ax.text(0.69, 0.54, f'Minimum Lattice (1500 ts): \n {round(min_lattice_1500, 6)}',
                        transform=ax.transAxes, verticalalignment='top', bbox=props)
                ax.text(0.69, 0.41, f'Minimum Energy (1500 ts): \n {round(min_energy_1500, 6)}',
                        transform=ax.transAxes, verticalalignment='top', bbox=props)

                plt.title(f'Lattice Parameter vs Energy at Composition {(0.50-conc):.2f}-Ni {(0.50+conc):.2f}-Ti')
                plt.legend()
                plt.show()

                # -------- Saving results
                output_dir = os.path.join(defect_path_sim, temp_dir)
                os.makedirs(output_dir, exist_ok=True)

                output_file_1000 = os.path.join(output_dir, f'Lattice_vs_Energy {atom_type1}{(0.50-conc):.2f}{atom_type2}{(0.50+conc):.2f} - 1000 timesteps.xlsx')
                output_file_1500 = os.path.join(output_dir, f'Lattice_vs_Energy {atom_type1}{(0.50-conc):.2f}{atom_type2}{(0.50+conc):.2f} - 1500 timesteps.xlsx')

                df_1000 = pd.DataFrame(energies_array_1000, columns=['Lattice Parameter', 'Energy'])
                df_1500 = pd.DataFrame(energies_array_1500, columns=['Lattice Parameter', 'Energy'])

                df_1000.to_excel(output_file_1000)
                df_1500.to_excel(output_file_1500)

                print(f"Results saved in: {output_file_1000} and {output_file_1500}")

