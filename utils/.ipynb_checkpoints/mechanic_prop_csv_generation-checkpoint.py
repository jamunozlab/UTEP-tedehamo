import os
import pandas as pd
from utils.config import mechanical_path

def csv_mechanical_properties(
    rows_df,
    configurational_entropy,
    concentrations,
    atom_type1,
    atom_type2,
    defect_label,
    defect_percentages,
    reduction_percentages,
    base_params_atoms_position
):
    mech_prop_df = pd.DataFrame(rows_df)
    entropy_df = pd.DataFrame(configurational_entropy)

    entropy_stacked = []
    for defe in defect_label:
        entropy_df[defe] = entropy_df[defe].apply(lambda x: x[0] if isinstance(x, list) else x)
        repeated = pd.concat([entropy_df[defe]] * base_params_atoms_position['n_temp_variations'], axis=0).reset_index(drop=True)
        entropy_stacked.append(repeated)

    conf_entropy_df = pd.DataFrame({
        'configurational_entropy': pd.concat(entropy_stacked, axis=0).reset_index(drop=True)
    })

    Al_conc = pd.DataFrame(concentrations[atom_type1], columns=[f'{atom_type1}_composition'])
    Fe_conc = pd.DataFrame(concentrations[atom_type2], columns=[f'{atom_type2}_composition'])

    mech_prop_df = pd.concat([Al_conc, Fe_conc, mech_prop_df, conf_entropy_df], axis=1)

    for temp in range(base_params_atoms_position['n_temp_variations']):
        for defect in range(len(defect_percentages)):
            ii = temp * len(defect_percentages) + defect
            start = ii * len(reduction_percentages)
            end = start + len(reduction_percentages)
            df_slice = mech_prop_df.iloc[start:end].copy()

            T = base_params_atoms_position["initial_temperature"] + temp * 100
            rename = {
                'internal_energy': f'internal_energy_{T}K_ord',
                'internal_energy_error': f'internal_energy_{T}K_ord_error',
                'bulk_modulus': f'bulk_modulus_{T}K_ord',
                'bulk_modulus_error': f'bulk_modulus_{T}K_ord_error',
                'bulk_modulus_prime': f'bulk_modulus_derivative_{T}K_ord',
                'bulk_modulus_prime_error': f'bulk_modulus_derivative_{T}K_ord_error',
                'lattice_parameter': f'lattice_parameter_{T}K_ord',
                'lattice_parameter_error': f'lattice_parameter_{T}K_ord_error',
                'configurational_entropy': f'configurational_entropy_{T}K_ord'
            }

            df_slice.rename(columns=rename, inplace=True)

            df_slice[f'bulk_modulus_{T}K_ord_up'] = df_slice[f'bulk_modulus_{T}K_ord'] + df_slice[f'bulk_modulus_{T}K_ord_error']
            df_slice[f'bulk_modulus_{T}K_ord_down'] = df_slice[f'bulk_modulus_{T}K_ord'] - df_slice[f'bulk_modulus_{T}K_ord_error']
            df_slice[f'bulk_modulus_derivative_{T}K_ord_up'] = df_slice[f'bulk_modulus_derivative_{T}K_ord'] + df_slice[f'bulk_modulus_derivative_{T}K_ord_error']
            df_slice[f'bulk_modulus_derivative_{T}K_ord_down'] = df_slice[f'bulk_modulus_derivative_{T}K_ord'] - df_slice[f'bulk_modulus_derivative_{T}K_ord_error']

            df_slice.drop(columns=['volume', 'volume_error', 'defect_label', 'temperature'], inplace=True)

            columns_order = list(df_slice.columns)
            for col in [
                f'bulk_modulus_{T}K_ord_up',
                f'bulk_modulus_{T}K_ord_down',
                f'bulk_modulus_derivative_{T}K_ord_up',
                f'bulk_modulus_derivative_{T}K_ord_down'
            ]:
                columns_order.remove(col)
            columns_order.insert(6, f'bulk_modulus_{T}K_ord_up')
            columns_order.insert(7, f'bulk_modulus_{T}K_ord_down')
            columns_order.insert(10, f'bulk_modulus_derivative_{T}K_ord_up')
            columns_order.insert(11, f'bulk_modulus_derivative_{T}K_ord_down')

            df_slice = df_slice[columns_order]

            # Save CSV
            os.makedirs(mechanical_path, exist_ok=True)
            filename = f'mech_prop_temp_{T}_def_{defect}.csv'
            df_slice.to_csv(os.path.join(mechanical_path, filename), index=False)

            print('--------------------------------------------------------------------------------')
            print(df_slice)
