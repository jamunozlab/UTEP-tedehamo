# UTEP-tedehamo
This code enables high-throughput pipelines for thousands of classical Molecular Dynamics (MD) simulations using LAMMPS, where parameters like temperature, concentration, system size, and the presence of point defects are fully automated.

It is an extended version of tedehamo https://github.com/jamunozlab/tedehamo, designed to not only run simulations but also extract mechanical and thermal properties from the MD results. The framework modularizes each step, including the computation of Warren-Cowley parameters and configurational entropy.

A simple example using an Iron-Aluminum alloy is provided to demonstrate functionality.

# Required Python Libraries

Make sure you have the following Python libraries installed:

- `numpy`
- `pandas`
- `json`
- `os`
- `subprocess`

---

# Workflow Overview

The main workflow starts from the **`Experiments.ipynb`** Jupyter notebook located in the root directory. This notebook provides a complete pipeline framework to generate all the necessary input files **before running your simulations**.

### Input Files Generated:

- **LAMMPS input file:** Contains simulation details such as temperature, thermostat, timestep size, number of timesteps, etc.
- **Atom positions file:** Includes information about the crystal structure, initial atomic positions, and structure type.
- **SBATCH file:** Script tailored for the NERSC Perlmutter supercomputer, specifying GPU job parameters.
- **LAMMPS executable:** MPI-compatible executable for running simulations.

---

# How It Works

1. The code first creates a **JSON directory**, where each file defines the settings of a specific simulation.
2. These JSON files are parsed to automatically generate:
   - the LAMMPS input script,
   - atomic positions,
   - and SBATCH submission files.
3. All necessary files are copied into a designated output directory.
4. The job is submitted using the `sbatch` command on **Perlmutter**.  
   *(If you're running on a local machine, just **uncomment the relevant lines in the notebook**.)*

The main loops iterate over:
- **Point defects**
- **Temperatures**
- **Concentrations**

These parameters are defined in `utils/default_dictionaries.py` and can be easily customized.

Path configurations, atom types, and general settings are defined in `utils/config.py`.

You must also provide an **interatomic potential** (e.g., from NIST).  
This example uses **2NN-MEAM potentials**, available at:  
📄 [DOI: 10.1016/j.commatsci.2021.110902](https://doi.org/10.1016/j.commatsci.2021.110902)
And they must be inside the Potentials directory.

---

# Post-Processing

Once your simulations are complete, move on to the **`Post-processing.ipynb`** notebook.

### What it does:
- Uses the `extracting_energies_before_BM()` function to collect internal energy values at timesteps 1500 and 2000.
- Performs a **Birch-Murnaghan fit** to extract:
  - Equilibrium volume
  - Bulk modulus
  - Internal energy
  - Pressure derivative of the bulk modulus

The results are:
- Saved in separate directories for each temperature and defect level
- Plotted to visually verify the fit and physical trends

---

# Additional Calculations

Before calculating thermal properties:
- Compute **Warren-Cowley short-range order parameters** and **configurational entropy**, this by Using https://github.com/killiansheriff/WarrenCowleyParameters.
- Organize your input files by temperature and defect points

A utility function is available to **sort and save parameters to CSV files**, ensuring compatibility with thermal property calculations.

---

# Thermal Properties

The final step is to compute thermal properties using the `error_calculation()` function located in `utils/thermal_prop_cal.py`.

This function is embedded in nested loops over **defect percentages** and **temperatures** in the notebook, and it:
- Reads mechanical property CSVs
- Computes error propagation
- Outputs thermal property results

---
