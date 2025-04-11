import numpy as np
def configurational_entropy_function(c1, c2, NiTi, NiNi, TiTi, TiNi):
    S = 0.0  # Initialize entropy
    
    if NiNi != 1:
        term1 = (c1 * c1) * (1 - NiNi) * np.nan_to_num(np.log(1 + (c2 / c1) * (1 - TiNi) / (1 - NiNi)))
        S += term1
    
    if NiTi != 1:
        term2 = (c1 * c2) * (1 - NiTi) * np.nan_to_num(np.log(1 + (c2 / c1) * (1 - TiTi) / (1 - NiTi)))
        S += term2
    
    if TiTi != 1:
        term3 = (c2 * c2) * (1 - TiTi) * np.nan_to_num(np.log(1 + (c1 / c2) * (1 - NiTi) / (1 - TiTi)))
        S += term3
    
    if TiNi != 1:
        term4 = (c2 * c1) * (1 - TiNi) * np.nan_to_num(np.log(1 + (c1 / c2) * (1 - NiNi) / (1 - TiNi)))
        S += term4

    return S

    
    
    # Define the entropy calculation function
# def configurational_entropy_function(c1, c2, NiTi, NiNi, TiTi, TiNi):
#     S = ((c1*c1)*(1-NiNi)*np.nan_to_num(np.log(1 + (c2/c1)*(1-TiNi)/(1-NiNi))) + 
#          (c1*c2)*(1-NiTi)*np.nan_to_num(np.log(1 + (c2/c1)*(1-TiTi)/(1-NiTi))) + 
#          (c2*c2)*(1-TiTi)*np.nan_to_num(np.log(1 + (c1/c2)*(1-NiTi)/(1-TiTi))) +  
#          (c2*c1)*(1-TiNi)*np.nan_to_num(np.log(1 + (c1/c2)*(1-NiNi)/(1-TiNi))))
#     return S