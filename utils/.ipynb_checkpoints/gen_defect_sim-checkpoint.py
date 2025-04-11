import numpy as np
import pandas as pd

def generate_atom_type_array(total_atoms):
    """Generates an atom type array for an initial B2 ordered structure."""
    atom_type_array = np.zeros(total_atoms, dtype=int)
    for i in range(total_atoms):
        atom_type_array[i] = 2 if (i + 1) % 2 == 0 else 1
    
    num_type_1 = np.sum(atom_type_array == 1)
    num_type_2 = np.sum(atom_type_array == 2)
    
    return atom_type_array, num_type_1, num_type_2

# def reduce_concentration(atom_type_array, atom_type_to_reduce, reduction_percentage):
#     """Reduces the concentration of a specific atom type based on a given percentage."""
#     indices_to_reduce_concentration = np.where(atom_type_array == atom_type_to_reduce)[0]
#     num_to_reduce_concentration = int(len(indices_to_reduce_concentration) * 2 * reduction_percentage)
    
#     if num_to_reduce_concentration >= 0:
#         indices_selected_concentration = np.random.choice(
#             indices_to_reduce_concentration, num_to_reduce_concentration, replace=False)
#         atom_type_array[indices_selected_concentration] = 2  # Change to type 2

#     if num_to_reduce_concentration < 0:
#         indices_selected_concentration = np.random.choice(
#             indices_to_reduce_concentration, num_to_reduce_concentration, replace=False)
#         atom_type_array[indices_selected_concentration] = 1  # Change to type 1
        
#     num_type_1 = np.sum(atom_type_array == 1)
#     num_type_2 = np.sum(atom_type_array == 2)
    
#     return atom_type_array, num_type_1, num_type_2


import numpy as np
def reduce_concentration(atom_type_array, atom_type_to_reduce, reduction_percentage):
    """
    Adjust concentration by reducing or increasing the target atom type.
    Positive percentage → reduce the target type.
    Negative percentage → increase the target type by reducing the other.
    """
    atom_type_to_reduce = int(atom_type_to_reduce)
    atom_type_array = np.array(atom_type_array)

    if atom_type_to_reduce not in [1, 2]:
        raise ValueError("Only supports atom types 1 and 2.")

    other_type = 2 if atom_type_to_reduce == 1 else 1
    
    from_type = atom_type_to_reduce
    to_type = other_type
    # if reduction_percentage == 0:
    #     return atom_type_array, np.sum(atom_type_array == 1), np.sum(atom_type_array == 2)

    # if reduction_percentage > 0:
    #     from_type = atom_type_to_reduce
    #     to_type = other_type
    # else:
    #     from_type = other_type
    #     to_type = atom_type_to_reduce

    indices_to_modify = np.where(atom_type_array == from_type)[0]
    num_to_change = int(len(atom_type_array) * abs(reduction_percentage))

    # print(f"Changing {num_to_change} atoms from type {from_type} → {to_type}")

    if num_to_change > len(indices_to_modify):
        raise ValueError("Too few atoms to change.")

    if num_to_change == 0:
        print("No atoms changed due to small reduction_percentage.")
        return atom_type_array, np.sum(atom_type_array == 1), np.sum(atom_type_array == 2)

    selected_indices = np.random.choice(indices_to_modify, num_to_change, replace=False)
    atom_type_array[selected_indices] = to_type

    return atom_type_array, np.sum(atom_type_array == 1), np.sum(atom_type_array == 2)


def introduce_vacancies(atom_type_array, atom_type_to_remove, vacancy_percentage):
    """Introduces vacancies by removing a percentage of atoms of a specific type."""
    indices_to_remove_vacancy = np.where(atom_type_array == atom_type_to_remove)[0]
    num_to_remove_vacancy = int(len(indices_to_remove_vacancy) * (vacancy_percentage / 100))
    
    if num_to_remove_vacancy > 0:
        indices_selected_vacancy = np.random.choice(
            indices_to_remove_vacancy, num_to_remove_vacancy, replace=False)
        atom_type_array = np.delete(atom_type_array, indices_selected_vacancy)
        
    num_type_1 = np.sum(atom_type_array == 1)
    num_type_2 = np.sum(atom_type_array == 2)
    
    return atom_type_array,  num_type_1, num_type_2

# def generate_defect_positions(total_atoms, atom_type_array, defect_percentage):
#     """Generates defect positions based on the given defect percentage."""
#     total_order_defects = int(total_atoms * defect_percentage / 100)
#     range_total_atoms = atom_type_array #-- np.arange(1, total_atoms + 1)
#     random_defects_array = np.random.choice(range_total_atoms, total_order_defects, replace=False)
#     # df_random_positions = pd.DataFrame(random_defects_array, columns=['Defect Positions'])
#     num_type_1 = np.sum(random_defects_array == 1)
#     num_type_2 = np.sum(random_defects_array == 2)
#     return random_defects_array,  num_type_1, num_type_2

# def generate_defect_positions(total_atoms, atom_type_array, defect_percentage):
#     """Generates defect positions based on the given defect percentage and swaps those atoms."""
    
#     total_order_defects = int(total_atoms * defect_percentage / 100)
#     range_total_atoms = atom_type_array  
    
#     random_defects_array = np.random.choice(range_total_atoms, total_order_defects, replace=False)
    
#     num_type_1 = np.sum(random_defects_array == 1)
#     num_type_2 = np.sum(random_defects_array == 2)
    
#     modified_atom_type_array = atom_type_array.copy()
    
#     # Swap selected atoms by replacing them with the other type
#     for pos in random_defects_array:
#         if modified_atom_type_array[pos] == 1:
#             modified_atom_type_array[pos] = 2
#         elif modified_atom_type_array[pos] == 2:
#             modified_atom_type_array[pos] = 1
    
#     return modified_atom_type_array, random_defects_array, num_type_1, num_type_2

def generate_defect_positions(total_atoms, atom_type_array, defect_percentage):
    
    total_defects = int(total_atoms * defect_percentage / 100)
    
    indices_type_1 = np.where(atom_type_array == 1)[0] 
    indices_type_2 = np.where(atom_type_array == 2)[0]  

    num_defects_1 = int(len(indices_type_1) * defect_percentage / 100)
    num_defects_2 = int(len(indices_type_2) * defect_percentage / 100)

    defect_indices_1 = np.random.choice(indices_type_1, num_defects_1, replace=False)
    defect_indices_2 = np.random.choice(indices_type_2, num_defects_2, replace=False)

    modified_atom_type_array = atom_type_array.copy()

    modified_atom_type_array[defect_indices_1] = 2  
    modified_atom_type_array[defect_indices_2] = 1 
    
    num_type_1 = np.sum(modified_atom_type_array == 1)
    num_type_2 = np.sum(modified_atom_type_array == 2)

    return modified_atom_type_array, defect_indices_1, defect_indices_2, num_type_1, num_type_2
