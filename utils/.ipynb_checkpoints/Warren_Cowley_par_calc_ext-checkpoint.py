from utils.config import atom_type1
from utils.conf_entropy import configurational_entropy_function
from utils.default_dictionaries import nneigh
from ovito.io import import_file
import WarrenCowleyParameters as wc
import matplotlib.pyplot as plt

def calculate_warren_cowley_and_entropy(pre_conf_entr_cal_dict, 
                                        atom_type1, atom_type2, 
                                        defect_percentages, 
                                        reduction_percentages):
    interactions = {
        f'{atom_type1}{atom_type2}': {},
        f'{atom_type1}{atom_type1}': {},
        f'{atom_type2}{atom_type1}': {},
        f'{atom_type2}{atom_type2}': {}
    }

    configurational_entropy = {}

    for defect in defect_percentages:
        defect_key = f'{defect}%'
        for key in interactions:
            interactions[key][defect_key] = {}
        configurational_entropy[defect_key] = {}

        for conc in reduction_percentages:
            conc_key = 50 - conc * 100
            conc_int = int(conc * 100)

            for key in interactions:
                interactions[key][defect_key][conc_key] = []

            configurational_entropy[defect_key][conc_key] = []

            pipeline = import_file(pre_conf_entr_cal_dict[defect_key]['500'][conc_int])
            mod = wc.WarrenCowleyParameters(nneigh=nneigh, only_selected=False)
            pipeline.modifiers.append(mod)
            data = pipeline.compute()

            wc_for_shells = data.attributes["Warren-Cowley parameters"]

            interactions[f'{atom_type1}{atom_type2}'][defect_key][conc_key].append(wc_for_shells[3][0][0])
            interactions[f'{atom_type1}{atom_type1}'][defect_key][conc_key].append(wc_for_shells[3][1][1])
            interactions[f'{atom_type2}{atom_type1}'][defect_key][conc_key].append(wc_for_shells[2][0][0])
            interactions[f'{atom_type2}{atom_type2}'][defect_key][conc_key].append(wc_for_shells[2][1][1])

            if conc >= 0.5:
                configurational_entropy[defect_key][conc_key].append(
                    configurational_entropy_function(0.50 - conc, 0.50 + conc,
                                                     wc_for_shells[3][0][0],
                                                     wc_for_shells[3][1][1],
                                                     wc_for_shells[2][0][0],
                                                     wc_for_shells[3][0][0])
                )
            else:
                configurational_entropy[defect_key][conc_key].append(
                    configurational_entropy_function(0.50 - conc, 0.50 + conc,
                                                     wc_for_shells[3][1][1],
                                                     wc_for_shells[3][1][1],
                                                     wc_for_shells[3][0][0],
                                                     wc_for_shells[3][0][0])
                )

    return interactions, configurational_entropy


def plot_warren_cowley_interactions(interactions,
                                     atom_type1,
                                     atom_type2,
                                     defect_percentages,
                                     colors_plot,
                                     markers_plot):

    interaction_types = [
        f'{atom_type1}{atom_type2}',
        f'{atom_type1}{atom_type1}',
        f'{atom_type2}{atom_type1}',
        f'{atom_type2}{atom_type2}'
    ]

    fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    axs = axs.flatten()

    for idx, interaction in enumerate(interaction_types):
        ax = axs[idx]
        for i, defect in enumerate(defect_percentages):
            defect_key = f'{defect}%'
            concentrations = sorted(interactions[interaction][defect_key].keys()) 
            wc_values = [interactions[interaction][defect_key][c][0] for c in concentrations] 

            ax.plot(concentrations, wc_values,
                    label=f'Defect {defect}%',
                    color=colors_plot[i % len(colors_plot)],
                    marker=markers_plot[i % len(markers_plot)],
                    linewidth=2)

        ax.set_title(f'Interaction: {interaction}', fontsize=12)
        ax.set_ylabel('Warren-Cowley Parameter', fontsize=11)
        ax.grid(True)
        ax.legend()

    axs[2].set_xlabel(f'{atom_type1} Concentration (%)')
    axs[3].set_xlabel(f'{atom_type1} Concentration (%)')
    
    plt.tight_layout()
    plt.show()


def plot_configurational_entropy(configurational_entropy,
                                 xlabel=f'Concentration of {atom_type1} (%)',
                                 ylabel='Configurational Entropy ',
                                 title='Configurational Entropy vs Ni Concentration',
                                 invert_x=True):
    """
    Plots the configurational entropy vs Ni concentration for different defect levels.

    Parameters:
        configurational_entropy (dict): Dictionary with entropy values by defect percentage.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        title (str): Plot title.
        invert_x (bool): Whether to invert the x-axis (default: True).

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))

    for defect, values in configurational_entropy.items():
        concentrations = list(values.keys())
        entropies = [v[0] for v in values.values()]
        plt.plot(concentrations, entropies, marker='o', label=f'Defect {defect}')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if invert_x:
        plt.gca().invert_xaxis()

    plt.show()
