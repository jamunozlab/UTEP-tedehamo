import os

def write_sbatch(simulation_dir, input_filename, slurm_config):
    """
    Writes a SLURM batch script for a specific simulation, replacing the input filename in the command.

    Parameters:
    - simulation_dir (str): Directory where the SLURM script will be saved.
    - input_filename (str): Name of the LAMMPS input file (e.g., 'NiTi_1.in').
    - slurm_config (dict): Dictionary containing SLURM job settings.
    """
    os.makedirs(simulation_dir, exist_ok=True)
    
    sbatch_filename = os.path.join(simulation_dir, "run.sbatch")

    slurm_command = slurm_config["command"].format(input_filename)

    with open(sbatch_filename, "w") as sbatch_file:
        sbatch_file.write("#!/bin/bash\n")
        sbatch_file.write(f"#SBATCH --image {slurm_config['image']}\n")
        sbatch_file.write(f"#SBATCH -A {slurm_config['account']}\n")
        sbatch_file.write(f"#SBATCH -C {slurm_config['constraint']}\n")
        sbatch_file.write(f"#SBATCH -q {slurm_config['queue']}\n")
        sbatch_file.write(f"#SBATCH -J {slurm_config['job_name']}\n")
        sbatch_file.write(f"#SBATCH -o {slurm_config['output_file']}\n")
        sbatch_file.write(f"#SBATCH -t {slurm_config['time_limit']}\n")
        sbatch_file.write(f"#SBATCH -c {slurm_config['cpus_per_task']}\n")
        sbatch_file.write(f"#SBATCH --gpus-per-task={slurm_config['gpus_per_task']}\n")
        sbatch_file.write(f"#SBATCH -n {slurm_config['num_tasks']}\n")
        sbatch_file.write("\n")
        sbatch_file.write(f"{slurm_command}\n")

    print(f"SLURM script written: {sbatch_filename}")
    return sbatch_filename
