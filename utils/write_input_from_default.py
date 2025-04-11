"""
Auxiliary functions to write lammps input files
"""
import os
import json
def write_lammps_input(data, filename):
    with open(filename, 'w') as f:
        f.write(f'units           {data["units"]}\n')
        f.write(f'dimension       {data["dimension"]}\n')
        f.write(f'boundary        {data["boundary"]}\n')
        f.write(f'atom_style      {data["atom_style"]}\n\n')
        f.write(f'read_data       {data["read_data"]}\n\n')
        
        # f.write(f'lattice         {data["lattice"]["type"]} {data["lattice"]["constant"]}\n')
        # region = data['region']
        # f.write(f'region          {region["name"]} {region["type"]} {" ".join(map(str, region["bounds"]))}\n')

        # f.write(f'create_box      {data["create_box"]["num_types"]} {data["create_box"]["region"]}\n')
        # f.write(f'create_atoms    {data["create_atoms"]["num_type"]} {data["create_atoms"]["region"]}\n\n')

        f.write(f'pair_style {data["pair_style"]}\n')
        f.write(f'pair_coeff {data["pair_coeff"]}\n')

        eq = data['equilibration']
        f.write('\n############################ EQUILIBRATION ############################\n')
        f.write(f'reset_timestep {eq["reset_timestep"]}\n')
        f.write(f'timestep {eq["timestep"]}\n')
        f.write(f'minimize {eq["minimize"]["etol"]} {eq["minimize"]["ftol"]} {eq["minimize"]["maxiter"]} {eq["minimize"]["maxeval"]}\n')

        dump_min = eq['dump_min']
        f.write(f'dump min all custom {dump_min["every"]} {dump_min["filename"]} {dump_min["attributes"]}\n')
        f.write(f'dump_modify min pbc {dump_min["modify"]["pbc"]} sort {dump_min["modify"]["sort"]}\n')

        dump_4a = eq['dump_4a']
        f.write(f'dump 4a all custom {dump_4a["every"]} {dump_4a["filename"]} {dump_4a["attributes"]}\n')
        f.write(f'dump_modify 4a pbc {dump_4a["modify"]["pbc"]} sort {dump_4a["modify"]["sort"]}\n')

        md = data['md_settings']
        f.write('\n##################### MD ##########################\n')
        f.write(f'reset_timestep     {md["reset_timestep"]}\n\n')

        vel = md['velocity']['all']
        f.write(f'velocity all create {vel["create"][0]} {vel["create"][1]} mom {vel["mom"]} rot {vel["rot"]}\n\n')
        f.write(f'reset_timestep     {md["reset_timestep"]}\n\n')
        fix = md['fix']
        f.write(f'fix {fix["id"]} {fix["group"]} {fix["style"]} temp {" ".join(map(str, fix["temp"]))}\n\n')

        f.write(f'thermo {md["thermo"]}\n')
        f.write(f'run     {md["run"]}\n\n')

        f.write('#---- SIMULATION DONE\n#---- Now go grab a coffee and pretend everything went exactly as planned ;).\n print All done ')
        f.write('print "All done"')
# -------------------------------------------------------

def generate_experiments_jsons_files(base_params, output_dir, mode="defect_reduction", defect_percentages=None, vacancy_percentages=None, reduction_percentages=None):
    """
    Generates JSON files for simulation parameters based on variations in defect, vacancy, and reduction percentages.

    Parameters:
    - base_params (dict): Dictionary containing base parameters for the simulations.
    - output_dir (str): Directory where the JSON files will be stored.
    - mode (str): Determines which parameters to use. Options:
        - "defect_reduction" (default) → Uses defect and reduction percentages.
        - "vacancy_reduction" → Uses vacancy and reduction percentages.
    - defect_percentages (list, optional): List of defect percentage values (only used in 
    "defect_reduction" mode).
    - vacancy_percentages (list, optional): List of vacancy percentage values (only used in 
    "vacancy_reduction" mode).
    - reduction_percentages (list): List of reduction percentage values to iterate over.
    """

    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

    if mode == "antisite":
        if defect_percentages is None:
            raise ValueError("defect_percentages must be provided in 'defect_reduction' mode.")
        for defect in defect_percentages:
            for reduction in reduction_percentages:
                params = base_params.copy()

                params['defect_percentage'] = defect
                params['reduction_percentage'] = reduction

                concentration_low = 0.50  +  reduction
                concentration_high = 0.50 - reduction

                # params['new_parent_dir'] = params['new_parent_dir_template'].format(
                #     concentration_high, concentration_low, defect
                # )

                json_filename = os.path.join(
                    output_dir,
                    f'param_experiments_conc{concentration_high:.2f}-{concentration_low:.2f}_defect_{defect}%.json'
                )
# f'param_experiments_conc0.{50+fil}-0.{50-fil}_vacancy_{vac}%.json'
                with open(json_filename, 'w') as json_file:
                    json.dump(params, json_file, indent=4)

                print(f"Created {json_filename}")

    elif mode == "vacancy":
        if vacancy_percentages is None:
            raise ValueError("vacancy_percentages must be provided in 'vacancy_reduction' mode.")
        for vacancy in vacancy_percentages:
            for reduction in reduction_percentages:
                params = base_params.copy()

                params['vacancy_percentage'] = vacancy
                params['reduction_percentage'] = reduction

                concentration_low = 0.50 +  reduction
                concentration_high = 0.50 -  reduction

                # params['new_parent_dir'] = params['new_parent_dir_template'].format(
                #     concentration_high, concentration_low, vacancy
                # )

                json_filename = os.path.join(
                    output_dir,
                    f'simulation_conc{concentration_high:.2f}-{concentration_low:.2f}_vacancy_{vacancy}%.json'
                )

                with open(json_filename, 'w') as json_file:
                    json.dump(params, json_file, indent=4)

                print(f"Created {json_filename}")

    else:
        raise ValueError("Invalid mode. Use 'defect_reduction' or 'vacancy_reduction'.")





