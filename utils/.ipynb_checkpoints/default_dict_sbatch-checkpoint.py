slurm_job_sbatch_dict = {
    "image": "docker:nersc/lammps_lite:23.08",
    "account": "m3845_g",
    "constraint": "gpu",
    "queue": "shared",
    "job_name": "LAMMPS_GPU",
    "output_file": "LAMMPS_GPU.o%j",
    "time_limit": "00:30:00",
    "cpus_per_task": 32,
    "gpus_per_task": 1,
    "num_tasks": 1,
    "command": "srun lmp_mpi -in {} > output.txt"
}

