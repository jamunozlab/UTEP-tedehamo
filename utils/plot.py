from utils.default_dictionaries import reduction_percentages, defect_percentages, base_params_atoms_position
import matplotlib.pyplot as plt
import pandas as pd

plt.figure(figsize=(15, 10), dpi=50)

def plot_mech_prop(Aluminium_concentration, parameter,  parameter_error, linestyles_plot, colors_plot, markers_plot,label_plot, defect,temperature_variation ):
    
    plt.errorbar(Aluminium_concentration[0:len(reduction_percentages)], parameter, yerr=parameter_error, 
                     fmt=markers_plot[defect_percentages.index(defect)], linestyle=linestyles_plot[defect_percentages.index(defect)], color=colors_plot[temperature_variation],  
                     markersize=22, markerfacecolor='none', linewidth=2.5, label=label_plot) 
    


